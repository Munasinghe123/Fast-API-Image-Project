from fastapi import UploadFile, HTTPException
from typing import List
from datetime import date
import hashlib
from pathlib import Path

from helpers.folder_creation_helper import get_raw_uploads_root
from controllers.db_image_controller import insert_image_record
from controllers.db_batch_controller import create_import_batch
from helpers.pole_sequence_helper import get_next_pole_sequence
from config.db_config import get_db_connection


async def upload_pole_images(
    poleCode: str,
    files: List[UploadFile]
):
    if not poleCode or not files:
        raise HTTPException(
            status_code=400,
            detail="poleCode and files are required"
        )

    pole_code = poleCode.strip().upper()

    raw_root = get_raw_uploads_root()
    pole_dir = raw_root / "Poles" / pole_code
    pole_dir.mkdir(parents=True, exist_ok=True)

    duplicates_skipped = 0
    new_files_exist = False
    temp_files = []

    # 1️⃣ Duplicate detection ONLY
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
        temp_files.append((file_bytes, file_hash, file.filename))

    if not new_files_exist:
        raise HTTPException(
            status_code=400,
            detail="All uploaded images are duplicates. Nothing saved."
        )

    # 2️⃣ Allocate GLOBAL sequence numbers
    sequences = get_next_pole_sequence(
        pole_code,
        count=len(temp_files),
        reset=False
    )

    # 3️⃣ Create batch
    batch_id = create_import_batch(
        source_folder=str(pole_dir),
        imported_by="system",
        total_images=len(temp_files)
    )

    today = date.today()
    saved_files = []

    # 4️⃣ Save files + DB records
    for (file_bytes, file_hash, original_name), seq in zip(temp_files, sequences):

        ext = Path(original_name).suffix.lower()
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

    # 5️⃣ Mark batch as imported
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