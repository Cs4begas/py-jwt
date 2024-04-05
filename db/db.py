from contextlib import contextmanager
from psycopg2 import pool
import psycopg2
from settings import Settings

class DB:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DB, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self, 'is_initialized'):  # Prevent reinitialization
            self.is_initialized = True
            try:
                self.threaded_postgreSQL_pool = pool.ThreadedConnectionPool(5, 20, 
                                                                            user=Settings.DB_USR,
                                                                            password=Settings.DB_PWD,
                                                                            host=Settings.DB_HOST,
                                                                            port=Settings.DB_PORT,
                                                                            database=Settings.DB_NAME)
                if self.threaded_postgreSQL_pool:
                    print("Connection pool created successfully using ThreadedConnectionPool")
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while connecting to PostgreSQL", error)
                self.threaded_postgreSQL_pool = None

    def close_connection_pool(self):
        if self.threaded_postgreSQL_pool:
            self.threaded_postgreSQL_pool.closeall()
            print("Threaded PostgreSQL connection pool is closed")


    @contextmanager
    def get_connection(self):
        connection = None
        try:
            connection = self.threaded_postgreSQL_pool.getconn()
            yield connection
        finally:
            if connection is not None:
                self.threaded_postgreSQL_pool.putconn(connection)