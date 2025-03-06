
from contextlib import contextmanager
import redis


class RedisManager:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(RedisManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self, 'is_initialized'):  # Prevent reinitialization
            self.is_initialized = True
            try:
                self.redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
                self.redis_client = redis.Redis(connection_pool=self.redis_pool)
                
                if self.redis_client:
                    print("Connection pool on Redis was created successfully")
            except (Exception, ConnectionError) as error:
                print("Error while connecting to Redis", error)
                self.redis_client = None
    
    def get_redis_client(self):
        return self.redis_client