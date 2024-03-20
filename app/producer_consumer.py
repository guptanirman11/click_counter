from flask import Flask, jsonify
from flask_cors import CORS
import redis
import threading
import time
from queue import Queue

app = Flask(__name__)
CORS(app)

# Initialize Redis connection
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Initialize a thread-safe queue for increment actions
increment_queue = Queue()

def fetch_db_value():
    # Use Redis GET. If the key doesn't exist, initialize it to 0.
    value = redis_conn.get('counter') or 0
    print(f'fetched: {value}')
    return int(value)

# Background thread function to periodically sync the counter value to the database
def consumer():
    """Consumer function that processes items from the queue."""
    while True:
        # Wait for an item from the queue
        increment = increment_queue.get()
        # Process the increment
        redis_conn.incrby('counter', increment)
        print(f"Processed increment: {increment}")
        # Indicate that the item has been processed
        increment_queue.task_done()


@app.route('/click', methods=['POST'])
def click():
    # Enqueue an increment action instead of directly incrementing the counter
    increment_queue.put(1)
    return jsonify({'message': 'Increment queued'}), 200

@app.route('/counter', methods=['GET'])
def get_counter():
    # Return the most up-to-date counter value from Redis
    current_counter = fetch_db_value()
    return jsonify({'counter': current_counter}), 200

if __name__ == '__main__':
    # Start the background thread
    threading.Thread(target=consumer, daemon=True).start()
    app.run(debug=True, use_reloader=False)
