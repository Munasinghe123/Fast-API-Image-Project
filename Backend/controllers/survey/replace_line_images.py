from fastapi import UploadFile, HTTPException
from typing import List
from datetime import date
from pathlib import Path
import hashlib

from helpers.folder_creation_helper import get_raw_uploads_root
from helpers.line_id_helper import build_line_id
from helpers.line_sequence_helper import get_next_line_sequence
from helpers.delete_line_images import delete_line_images
from helpers.publish_replace_helper import (
    delete_published_line_images,
    publish_line_images_from_raw
)
from controllers.db_batch_controller import create_import_batch
from controllers.db_image_controller import insert_image_record
from config.db_config import get_db_connection


async def replace_line_images(
    startPoleCode: str,
    endPoleCode: str,
    files: List[UploadFile]
):
    # --------------------------------------------------
    # 1. Validation
    # --------------------------------------------------
    if not startPoleCode or not endPoleCode:
        raise HTTPException(
            status_code=400,
            detail="startPoleCode and endPoleCode are required"
        )

    if not files:
        raise HTTPException(
            status_code=400,
            detail="No files uploaded"
        )

    line_id = build_line_id(startPoleCode, endPoleCode)

    # --------------------------------------------------
    # 2. Ensure line already exists (replace must be valid)
    # --------------------------------------------------
    conn = get_db_connection()
    cur = conn.cursor()
    start, end = line_id.split("_")

    cur.execute(
        """
        SELECT COUNT(*)
        FROM images
        WHERE category = 'LINE'
        AND UPPER(start_pole) = %s
        AND UPPER(end_pole) = %s
        """,
        (start, end)
    )
    count = cur.fetchone()[0]
    cur.close()
    conn.close()

    if count == 0:
        raise HTTPException(
            status_code=400,
            detail="No existing images found for this line to replace"
        )

    # --------------------------------------------------
    # 3. HARD DELETE existing RAW images + DB rows
    # --------------------------------------------------
    delete_line_images(line_id)

    # --------------------------------------------------
    # 4. Prepare RAW folder
    # --------------------------------------------------
    raw_root = get_raw_uploads_root()
    line_dir = raw_root / "LineSections" / line_id
    line_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # 5. Read files into memory (no duplicate check on replace)
    # --------------------------------------------------
    temp_files = []
    for file in files:
        file_bytes = await file.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        temp_files.append((file.filename, file_bytes, file_hash))

    # --------------------------------------------------
    # 6. 🔥 Allocate GLOBAL sequences (RESET MODE)
    # --------------------------------------------------
    sequences = get_next_line_sequence(
        line_id=line_id,
        count=len(temp_files),
        reset=True
    )
    # Example: [1, 2, 3]

    # --------------------------------------------------
    # 7. Create import batch
    # --------------------------------------------------
    batch_id = create_import_batch(
        source_folder=str(line_dir),
        imported_by="system",
        total_images=len(temp_files)
    )

    survey_date = date.today()
    saved_files = []

    # --------------------------------------------------
    # 8. Save RAW files + DB records
    # --------------------------------------------------
    for (filename, file_bytes, file_hash), seq in zip(temp_files, sequences):

        ext = Path(filename).suffix.lower()
        if not ext:
            raise HTTPException(
                status_code=400,
                detail="All files must have a valid extension"
            )

        formatted_seq = f"{seq:02d}"
        safe_name = f"{line_id}_{formatted_seq}{ext}"
        raw_path = line_dir / safe_name

        insert_image_record(
            file_hash=file_hash,
            original_filename=filename,
            raw_path=str(raw_path),
            category="LINE",
            survey_date=survey_date,
            batch_id=batch_id,
            pole_id=line_id,
            sequence_no=seq
        )

        with open(raw_path, "wb") as f:
            f.write(file_bytes)

        saved_files.append(safe_name)

    # --------------------------------------------------
    # 9. Mark batch as IMPORTED
    # --------------------------------------------------
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE import_batches
        SET status = 'IMPORTED'
        WHERE batch_id = %s
        """,
        (batch_id,)
    )
    conn.commit()
    cur.close()
    conn.close()

    # --------------------------------------------------
    # 10. 🔥 Replace PUBLISHED images (best-effort)
    # --------------------------------------------------
    try:
        delete_published_line_images(line_id)
        publish_line_images_from_raw(line_id)
    except Exception as e:
        # RAW is authoritative — do not rollback
        print(f"[WARN] Published replace failed for line {line_id}: {e}")

    # --------------------------------------------------
    # 11. Response
    # --------------------------------------------------
    return {
        "message": "Line images replaced successfully",
        "lineSection": line_id,
        "batch_id": batch_id,
        "filesSaved": saved_files
    }