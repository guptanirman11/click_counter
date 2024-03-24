import threading
import redis

class PullWorker:
    def __init__(self, host, port, db, increment_queue):
        self.redis_conn = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
        self.thread = threading.Thread(target=self._consumer, daemon=True)
        self.increment_queue = increment_queue

    def start(self):
        self.thread.start()

    # Using Encapsulation
    def _consumer(self):
        """Consumer function that processes items from the queue."""
        while True:
            if not self.increment_queue.empty():
                increment = self.increment_queue.get()
                self.redis_conn.incrby('counter', increment)
                print(f"Processed increment: {increment}")
                self.increment_queue.task_done()
