from psycopg2.extensions import connection

def create_import_batch(
    conn: connection,
    source_folder: str,
    imported_by: str,
    total_images: int
) -> int:
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO import_batches (
            source_folder,
            imported_by,
            total_images,
            status
        )
        VALUES (%s, %s, %s, %s)
        RETURNING batch_id
        """,
        (source_folder, imported_by, total_images, "IMPORTING")
    )

    batch_id = cur.fetchone()[0]
    conn.commit()
    cur.close()

    return batch_id

def update_duplicates_skipped(
    conn: connection,
    batch_id: int,
    duplicates_skipped: int
):
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE import_batches
        SET duplicates_skipped = %s
        WHERE batch_id = %s
        """,
        (duplicates_skipped, batch_id)
    )

    conn.commit()
    cur.close()