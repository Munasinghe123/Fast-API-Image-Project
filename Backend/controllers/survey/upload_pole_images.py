from fastapi import UploadFile, HTTPException
from typing import List
from datetime import date
import hashlib

from config.db_config import get_db_connection
from helpers.folder_creation_helper import get_raw_uploads_root
from controllers.db_image_controller import insert_image_record
from controllers.db_batch_controller import create_import_batch


async def upload_pole_images(
    poleCode: str,
    files: List[UploadFile]
):
    #  Validation 
    if not poleCode or not files:
        raise HTTPException(
            status_code=400,
            detail="poleCode and files are required"
        )

    pole_code = poleCode.strip().upper()

    raw_root = get_raw_uploads_root()
    pole_dir = raw_root / "Poles" / pole_code

    #  Get last sequence number 
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(MAX(sequence_no), 0)
        FROM images
        WHERE category = 'POLE'
        AND UPPER(pole_id) = %s
    """, (pole_code,))

    last_sequence = cur.fetchone()[0]

    cur.close()
    conn.close()

    today = date.today()
    current_sequence = last_sequence
    duplicates_skipped = 0
    saved_files = []
    new_files_exist = False

    file_data_list = []

    #  First pass: duplicate detection 
    for file in files:
        file_bytes = await file.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()

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

        raw_path = pole_dir / file.filename

        file_data_list.append((
            file.filename,
            file_bytes,
            file_hash,
            raw_path,
            current_sequence
        ))

    #  All duplicates case 
    if not new_files_exist:
        raise HTTPException(
            status_code=400,
            detail="All uploaded images are duplicates. Nothing saved."
        )

    #  Folder + batch creation 
    pole_dir.mkdir(parents=True, exist_ok=True)

    batch_id = create_import_batch(
        source_folder=str(pole_dir),
        imported_by="system",
        total_images=len(file_data_list)
    )

    #  Insert records + save files 
    for filename, file_bytes, file_hash, raw_path, sequence_no in file_data_list:

        insert_image_record(
            file_hash=file_hash,
            original_filename=filename,
            raw_path=str(raw_path),
            category="POLE",
            survey_date=today,
            batch_id=batch_id,
            pole_id=pole_code,
            sequence_no=sequence_no
        )

        with open(raw_path, "wb") as f:
            f.write(file_bytes)

        saved_files.append(filename)

    #  Mark batch as imported 
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

    return {
        "message": "Pole images uploaded successfully",
        "batch_id": batch_id,
        "filesSaved": saved_files,
        "duplicatesSkipped": duplicates_skipped
    }