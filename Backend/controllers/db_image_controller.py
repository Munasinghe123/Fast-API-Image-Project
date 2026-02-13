import psycopg2
from psycopg2.extensions import connection

def insert_image_record(
    conn: connection,
    file_hash,
    original_filename,
    raw_path,
    category,
    survey_date,
    batch_id,
    pole_id=None,
    start_pole=None,
    end_pole=None,
    sequence_no=None
) -> bool:
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO images (
                file_hash,
                original_filename,
                raw_path,
                category,
                survey_date,
                batch_id,
                pole_id,
                start_pole,
                end_pole,
                sequence_no
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (file_hash) DO NOTHING
            """,
            (
                file_hash,
                original_filename,
                raw_path,
                category,
                survey_date,
                batch_id,
                pole_id,
                start_pole,
                end_pole,
                sequence_no
            )
        )

        inserted = cur.rowcount == 1
        conn.commit()
        return inserted

    except psycopg2.Error:
        conn.rollback()
        raise

    finally:
        cur.close()