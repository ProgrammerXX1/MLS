import time
import psycopg2
import os

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = int(os.getenv("POSTGRES_PORT", 5432))
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "2123")
DB_NAME = os.getenv("POSTGRES_DB", "db")

while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            dbname=DB_NAME,
        )
        conn.close()
        print("✅ PostgreSQL is ready.")
        break
    except psycopg2.OperationalError:
        print("⏳ Waiting for PostgreSQL...")
        time.sleep(1)
