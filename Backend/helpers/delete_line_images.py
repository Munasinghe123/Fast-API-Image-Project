from pathlib import Path
import shutil

from config.db_config import get_db_connection
from helpers.folder_creation_helper import get_raw_uploads_root


def delete_line_images(line_id: str):
    """
    Hard delete ALL line images:
    - DB rows
    - RAW filesystem folder

    Does NOT touch:
    - sequence table
    - published folder (handled separately)
    """

    # ---------------- Delete DB records ----------------
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM images
        WHERE category = 'LINE'
        AND pole_id = %s
        """,
        (line_id,)
    )

    conn.commit()
    cur.close()
    conn.close()

    # ---------------- Delete RAW files ----------------
    raw_root = get_raw_uploads_root()
    line_dir = raw_root / "LineSections" / line_id

    if line_dir.exists():
        shutil.rmtree(line_dir)