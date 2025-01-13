import psycopg2

# Database connection details
DATABASE_CONFIG = {
    "host": "ep-icy-sunset-a5w4vk1z.us-east-2.aws.neon.tech",
    "database": "tkinter_app",
    "user": "tkinter_app_owner",
    "password": "StEJAv6Lp4Kc",
    "sslmode": "require"
}

# Connect to the database
try:
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    print("Connected to the database")

    # Create table SQL
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        age INT NOT NULL
    );
    """
    
    # Execute the query
    cursor.execute(create_table_query)
    conn.commit()
    print("Table created successfully")
except Exception as e:
    print("Error:", e)
finally:
    if conn:
        cursor.close()
        conn.close()
