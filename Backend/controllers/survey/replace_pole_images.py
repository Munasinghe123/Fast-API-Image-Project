from fastapi import UploadFile, HTTPException
from typing import List
from datetime import date
from pathlib import Path
import hashlib

from config.db_config import get_db_connection
from helpers.folder_creation_helper import get_raw_uploads_root
from helpers.delete_pole_images import delete_pole_images
from helpers.publish_replace_helper import (
    delete_published_pole_images,
    publish_pole_images_from_raw
)
from controllers.db_batch_controller import create_import_batch
from controllers.db_image_controller import insert_image_record
from helpers.pole_sequence_helper import get_next_pole_sequence


async def replace_pole_images_controller(
    poleCode: str,
    files: List[UploadFile]
):
    # --------------------------------------------------
    # 1. Validation
    # --------------------------------------------------
    if not poleCode or not files:
        raise HTTPException(
            status_code=400,
            detail="poleCode and files are required"
        )

    pole_code = poleCode.strip().upper()

    # --------------------------------------------------
    # 2. Ensure pole already exists (replace must be meaningful)
    # --------------------------------------------------
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM images
        WHERE category = 'POLE'
        AND UPPER(pole_id) = %s
    """, (pole_code,))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()

    if count == 0:
        raise HTTPException(
            status_code=400,
            detail="No existing images found for this pole to replace"
        )

    # --------------------------------------------------
    # 3. HARD DELETE existing RAW images + DB rows
    #    (Replace = delete the container)
    # --------------------------------------------------
    delete_pole_images(pole_code)

    # --------------------------------------------------
    # 4. Prepare RAW folder
    # --------------------------------------------------
    raw_root = get_raw_uploads_root()
    pole_dir = raw_root / "Poles" / pole_code
    pole_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # 5. Read all files into memory (no duplicates check on replace)
    # --------------------------------------------------
    temp_files = []
    for file in files:
        file_bytes = await file.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        temp_files.append((file_bytes, file_hash, file.filename))

    # --------------------------------------------------
    # 6. 🔥 Allocate sequence numbers (RESET MODE)
    #    This ALWAYS starts from 1
    # --------------------------------------------------
    sequences = get_next_pole_sequence(
        pole_code,
        count=len(temp_files),
        reset=True
    )
    # Example: [1, 2, 3]

    # --------------------------------------------------
    # 7. Create import batch
    # --------------------------------------------------
    batch_id = create_import_batch(
        source_folder=str(pole_dir),
        imported_by="system",
        total_images=len(temp_files)
    )

    today = date.today()
    saved_files = []

    # --------------------------------------------------
    # 8. Save RAW files + DB records
    # --------------------------------------------------
    for (file_bytes, file_hash, original_name), seq in zip(temp_files, sequences):

        ext = Path(original_name).suffix.lower()
        if not ext:
            raise HTTPException(
                status_code=400,
                detail="All files must have a valid extension"
            )

        formatted_seq = f"{seq:02d}"
        safe_name = f"{pole_code}_{formatted_seq}{ext}"
        raw_path = pole_dir / safe_name

        insert_image_record(
            file_hash=file_hash,
            original_filename=original_name,
            raw_path=str(raw_path),
            category="POLE",
            survey_date=today,
            batch_id=batch_id,
            pole_id=pole_code,
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
    cur.execute("""
        UPDATE import_batches
        SET status = 'IMPORTED'
        WHERE batch_id = %s
    """, (batch_id,))
    conn.commit()
    cur.close()
    conn.close()

    # --------------------------------------------------
    # 10. 🔥 Replace PUBLISHED images (best-effort)
    # --------------------------------------------------
    try:
        delete_published_pole_images(pole_code)
        publish_pole_images_from_raw(pole_code)
    except Exception as e:
        # Raw replace is authoritative – do not rollback
        print(f"[WARN] Published replace failed for pole {pole_code}: {e}")

    # --------------------------------------------------
    # 11. Response
    # --------------------------------------------------
    return {
        "message": "Pole images replaced successfully",
        "batch_id": batch_id,
        "filesSaved": saved_files
    }