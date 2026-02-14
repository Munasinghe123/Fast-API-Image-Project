from config.db_config import get_db_connection
import psycopg2


def insert_image_record(
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
):
    conn = get_db_connection()
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

        conn.commit()

    except psycopg2.Error:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()