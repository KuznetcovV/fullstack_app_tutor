import psycopg2

conn = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    user="postgres",
    password="postgres",
    dbname="fastapi_test_db",
)
cur = conn.cursor()
cur.execute("SELECT 1")
print("УСПЕХ:", cur.fetchone())
conn.close()