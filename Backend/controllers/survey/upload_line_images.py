from fastapi import UploadFile, HTTPException
from typing import List
from datetime import date
from pathlib import Path

from helpers.folder_creation_helper import get_raw_uploads_root
from helpers.line_id_helper import build_line_id
from helpers.line_sequence_helper import get_next_line_sequence
from controllers.db_batch_controller import create_import_batch
from controllers.db_image_controller import insert_image_record
from helpers.hash_helper import compute_sha256
from config.db_config import get_db_connection


async def upload_line_images(
    startPoleCode: str,
    endPoleCode: str,
    files: List[UploadFile]
):
    # ---------------- Validation ----------------
    if not startPoleCode:
        raise HTTPException(status_code=400, detail="startPoleCode is required")

    if not endPoleCode:
        raise HTTPException(status_code=400, detail="endPoleCode is required")

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    # ---------------- Normalize / Build line_id ----------------
    line_id = build_line_id(startPoleCode, endPoleCode)

    survey_root = get_raw_uploads_root()
    line_dir = survey_root / "LineSections" / line_id

    duplicates_skipped = 0
    new_files_exist = False
    survey_date = date.today()

    temp_files = []

    # ---------------- First pass: detect duplicates ONLY ----------------
    for file in files:
        file_bytes = await file.read()
        file_hash = compute_sha256(file_bytes)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM images WHERE file_hash = %s",
            (file_hash,)
        )
        exists = cur.fetchone()
        cur.close()
        conn.close()

        if exists:
            duplicates_skipped += 1
            continue

        new_files_exist = True
        temp_files.append((file.filename, file_bytes, file_hash))

    # ---------------- All duplicates ----------------
    if not new_files_exist:
        raise HTTPException(
            status_code=400,
            detail="All uploaded images are duplicates. Nothing saved."
        )

    # ---------------- Allocate GLOBAL sequences (APPEND) ----------------
    sequences = get_next_line_sequence(
        line_id=line_id,
        count=len(temp_files),
        reset=False
    )

    # ---------------- Folder + batch ----------------
    line_dir.mkdir(parents=True, exist_ok=True)

    batch_id = create_import_batch(
        source_folder=str(line_dir),
        imported_by="system",
        total_images=len(temp_files)
    )

    saved_files = []

    # ---------------- Insert + save ----------------
    for (filename, file_bytes, file_hash), sequence_no in zip(temp_files, sequences):

        ext = Path(filename).suffix.lower()
        formatted_seq = f"{sequence_no:02d}"
        safe_name = f"{line_id}_{formatted_seq}{ext}"
        raw_path = line_dir / safe_name

        insert_image_record(
            file_hash=file_hash,
            original_filename=filename,
            raw_path=str(raw_path),
            category="LINE",
            survey_date=survey_date,
            batch_id=batch_id,
            start_pole=line_id.split("_")[0],
            end_pole=line_id.split("_")[1],
            sequence_no=sequence_no
        )

        with open(raw_path, "wb") as f:
            f.write(file_bytes)

        saved_files.append(safe_name)

    # ---------------- Mark batch imported ----------------
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

    return {
        "message": "Line images uploaded successfully",
        "lineSection": line_id,
        "batch_id": batch_id,
        "duplicatesSkipped": duplicates_skipped,
        "filesSaved": saved_files
    }