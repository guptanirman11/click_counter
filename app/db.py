import redis

# # Initializing Redis connection
# def get_redis_connection():
#     return redis.StrictRedis(host='my-redis-cluster.0diz5e.ng.0001.use1.cache.amazonaws.com', port=6379, db=0, decode_responses=True)

# # Fetch the current value of the counter from Cache
# def fetch_db_value(redis_conn):
#     value = redis_conn.get('counter') or 0
#     print(f'Fetched: {value}')
#     return int(value)

# # Increment the counter
# def increment_counter(redis_conn, increment=1):
#     redis_conn.incrby('counter', increment)



class RedisClient:
    def __init__(self, host='my-redis-cluster.0diz5e.ng.0001.use1.cache.amazonaws.com', port=6379, db=0):
        self.redis_conn = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def fetch_db_value(self):
        value = self.redis_conn.get('counter') or 0
        print(f'Fetched: {value}')
        return int(value)

    def increment_counter(self, increment=1):
        self.redis_conn.incrby('counter', increment)
