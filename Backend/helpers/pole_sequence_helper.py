from config.db_config import get_db_connection


def get_next_pole_sequence(pole_code: str, count: int = 1, reset: bool = False):
    """
    Returns a list of sequence numbers to use.

    - reset=True → starts from 1
    - reset=False → continues from last
    """

    conn = get_db_connection()
    cur = conn.cursor()

    # Ensure row exists
    cur.execute("""
        INSERT INTO pole_image_sequences (pole_id, last_sequence)
        VALUES (%s, 0)
        ON CONFLICT (pole_id) DO NOTHING
    """, (pole_code,))

    # Lock row
    cur.execute("""
        SELECT last_sequence
        FROM pole_image_sequences
        WHERE pole_id = %s
        FOR UPDATE
    """, (pole_code,))

    last_seq = cur.fetchone()[0]

    if reset:
        start = 1
        new_last = count
    else:
        start = last_seq + 1
        new_last = last_seq + count

    # Update tracker
    cur.execute("""
        UPDATE pole_image_sequences
        SET last_sequence = %s
        WHERE pole_id = %s
    """, (new_last, pole_code))

    conn.commit()
    cur.close()
    conn.close()

    return list(range(start, start + count))