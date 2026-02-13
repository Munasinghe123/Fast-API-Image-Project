import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="drone_image_system",
        user="postgres",
        password="admin",
        port=5432
    )

def test_db_connection():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        print(" Database connection successful")
    except Exception as e:
        print("Database connection failed")
        print(str(e))
        raise
    finally:
        if conn:
            conn.close()