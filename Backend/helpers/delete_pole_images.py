import shutil
from pathlib import Path
from config.db_config import get_db_connection
from helpers.folder_creation_helper import get_raw_uploads_root


def delete_pole_images(pole_code: str):
    """
    HARD replace delete:
    - Deletes DB records for the pole
    - Deletes the ENTIRE raw pole directory
    """

    # 1. Delete DB records
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM images
        WHERE category = 'POLE'
        AND UPPER(pole_id) = %s
    """, (pole_code,))
    conn.commit()
    cur.close()
    conn.close()

    # 2. Delete entire raw folder (authoritative)
    raw_root = get_raw_uploads_root()
    pole_dir = raw_root / "Poles" / pole_code

    if pole_dir.exists():
        shutil.rmtree(pole_dir)