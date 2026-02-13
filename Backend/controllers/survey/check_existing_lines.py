from fastapi import HTTPException
from config.db_config import get_db_connection


def check_existing_lines(startPole: str, endPole: str):
    start_pole = startPole.strip().upper()
    end_pole = endPole.strip().upper()

    if not start_pole or not end_pole:
        raise HTTPException(
            status_code=400,
            detail="startPole and endPole are required"
        )

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM images
            WHERE category = 'LINE'
            AND UPPER(start_pole) = %s
            AND UPPER(end_pole) = %s
            """,
            (start_pole, end_pole)
        )

        count = cur.fetchone()[0]

        return {
            "exists": count > 0,
            "count": count
        }

    finally:
        cur.close()
        conn.close()