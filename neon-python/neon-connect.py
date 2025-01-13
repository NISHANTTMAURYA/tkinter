import os
from psycopg2 import pool
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the connection string from the environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in .env file")
    exit(1)

try:
    print(f"Attempting to connect to database...")
    
    # Create a connection pool
    connection_pool = pool.SimpleConnectionPool(
        1,  # Minimum number of connections
        10,  # Maximum number of connections
        dsn=DATABASE_URL
    )

    if connection_pool:
        print("Connection pool created successfully")
        
        # Get a connection from the pool
        conn = connection_pool.getconn()
        
        # Create a cursor object
        cur = conn.cursor()
        
        # Test the connection
        cur.execute('SELECT NOW();')
        time = cur.fetchone()[0]
        print('Current time:', time)
        
        # Close everything
        cur.close()
        connection_pool.putconn(conn)
        connection_pool.closeall()
        
except Exception as e:
    print(f"Error connecting to database: {e}")