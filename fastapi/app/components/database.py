from psycopg2.pool import ThreadedConnectionPool

MIN_DATABASE_POOL = 1
MAX_DATABASE_POOL = 2

DATABASE_CONNECT = {
    "host" : "127.0.0.1",
    "port" : 5432,
    "user" : "postgres",
    "password" : "dockerdb",
    "database" : "accomplishment"
}

db_pool = ThreadedConnectionPool(
            MIN_DATABASE_POOL, 
            MAX_DATABASE_POOL,
            **DATABASE_CONNECT
        )

async def get_db():
    try:
        conn = db_pool.getconn()
        if conn: yield conn
    finally:
        if conn: db_pool.putconn(conn)