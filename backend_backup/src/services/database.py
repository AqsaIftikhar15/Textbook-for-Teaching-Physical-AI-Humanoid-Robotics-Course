# src/services/database.py
from psycopg2 import pool
from src.config.settings import settings

# Create a connection pool
db_pool = pool.SimpleConnectionPool(
    1, 10,  # min and max connections
    settings.neon_db_url
)

def get_conn():
    return db_pool.getconn()

def release_conn(conn):
    db_pool.putconn(conn)
