from fastapi import UploadFile, HTTPException
from typing import List
from datetime import date

from Backend.helpers.folder_creation_helper import get_raw_uploads_root
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

    # ---------------- Normalize ----------------
    start_pole_code = startPoleCode.strip().upper()
    end_pole_code = endPoleCode.strip().upper()

    survey_root = get_raw_uploads_root()
    line_folder_name = f"{start_pole_code}_{end_pole_code}"
    line_dir = survey_root / "LineSections" / line_folder_name

    # ---------------- Get last sequence ----------------
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COALESCE(MAX(sequence_no), 0)
        FROM images
        WHERE category = 'LINE'
        AND UPPER(start_pole) = %s
        AND UPPER(end_pole) = %s
        """,
        (start_pole_code, end_pole_code)
    )

    last_sequence = cur.fetchone()[0]
    cur.close()
    conn.close()

    current_sequence = last_sequence
    duplicates_skipped = 0
    saved_files = []
    new_files_exist = False

    survey_date = date.today()
    file_data_list = []

    # ---------------- First pass: detect duplicates ----------------
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
        current_sequence += 1

        raw_path = line_dir / file.filename

        file_data_list.append((
            file.filename,
            file_bytes,
            file_hash,
            raw_path,
            current_sequence
        ))

    # ---------------- All duplicates ----------------
    if not new_files_exist:
        raise HTTPException(
            status_code=400,
            detail="All uploaded images are duplicates. Nothing saved."
        )

    # ---------------- Folder + batch ----------------
    line_dir.mkdir(parents=True, exist_ok=True)

    batch_id = create_import_batch(
        source_folder=str(line_dir),
        imported_by="system",
        total_images=len(file_data_list)
    )

    # ---------------- Insert + save ----------------
    for filename, file_bytes, file_hash, raw_path, sequence_no in file_data_list:

        insert_image_record(
            file_hash=file_hash,
            original_filename=filename,
            raw_path=str(raw_path),
            category="LINE",
            survey_date=survey_date,
            batch_id=batch_id,
            start_pole=start_pole_code,
            end_pole=end_pole_code,
            sequence_no=sequence_no
        )

        with open(raw_path, "wb") as f:
            f.write(file_bytes)

        saved_files.append(filename)

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
        "lineSection": line_folder_name,
        "batch_id": batch_id,
        "duplicatesSkipped": duplicates_skipped,
        "filesSaved": saved_files
    }