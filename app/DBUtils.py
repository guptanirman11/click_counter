import redis

class RedisClient:
    # Establishes the connection
    def __init__(self, host='my-redis-cluster.0diz5e.ng.0001.use1.cache.amazonaws.com', port=6379, db=0):
        self.redis_conn = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
       
    # Method to fetch the value
    def fetch_db_value(self):
        value = self.redis_conn.get('counter') or 0
        print(f'Fetched: {value}')
        return int(value)

    # Method to increment the counter
    def increment_counter(self, increment=1):
        self.redis_conn.incrby('counter', increment)

    # Method to reset counter value
    def reset_counter(self):
       self.redis_conn.set('counter', 0)
       print('Counter reset to 0')