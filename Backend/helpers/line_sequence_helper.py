from config.db_config import get_db_connection


def get_next_line_sequence(
    line_id: str,
    count: int,
    reset: bool = False
):
    conn = get_db_connection()
    cur = conn.cursor()

    # Ensure row exists
    cur.execute("""
        INSERT INTO line_image_sequences (line_id, last_sequence)
        VALUES (%s, 0)
        ON CONFLICT (line_id) DO NOTHING
    """, (line_id,))

    # Lock row
    cur.execute("""
        SELECT last_sequence
        FROM line_image_sequences
        WHERE line_id = %s
        FOR UPDATE
    """, (line_id,))

    last_seq = cur.fetchone()[0]

    if reset:
        start = 1
        new_last = count
    else:
        start = last_seq + 1
        new_last = last_seq + count

    cur.execute("""
        UPDATE line_image_sequences
        SET last_sequence = %s
        WHERE line_id = %s
    """, (new_last, line_id))

    conn.commit()
    cur.close()
    conn.close()

    return list(range(start, start + count))