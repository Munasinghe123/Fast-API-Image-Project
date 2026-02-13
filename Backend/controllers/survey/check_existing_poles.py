from fastapi import HTTPException
from config.db_config import get_db_connection


def check_existing_poles(poleCode: str):
    pole_code = poleCode.strip().upper()

    if not pole_code:
        raise HTTPException(
            status_code=400,
            detail="poleCode is required"
        )

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM images
            WHERE category = 'POLE'
            AND UPPER(pole_id) = %s
            """,
            (pole_code,)
        )

        count = cur.fetchone()[0]

        return {
            "exists": count > 0,
            "count": count
        }

    finally:
        cur.close()
        conn.close()