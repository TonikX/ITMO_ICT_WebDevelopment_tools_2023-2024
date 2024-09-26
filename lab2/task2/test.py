import psycopg

try:
    conn = psycopg.connect("dbname=test user=postgres password=yourpassword")
    print("Connection successful")
except Exception as e:
    print("Connection failed:", e)