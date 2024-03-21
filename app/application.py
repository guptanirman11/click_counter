from flask import Flask, jsonify, render_template
from flask_cors import CORS
import redis
import threading
import time
from queue import Queue

app = Flask(__name__)
application = app
CORS(application)

# Initializing Redis connection
redis_conn = redis.StrictRedis(host='my-redis-cluster.0diz5e.ng.0001.use1.cache.amazonaws.com', port=6379, db=0, decode_responses=True)

# Initializing a thread-safe queue for increment actions
increment_queue = Queue()

def fetch_db_value():
    # fetching value from Redis
    value = redis_conn.get('counter') or 0
    print(f'fetched: {value}')
    return int(value)

# Background thread function to periodically sync the counter value to the database
def consumer():
    """Consumer function that processes items from the queue."""
    while True:

        # Wait for an item from the queue
        if not increment_queue.empty():
            
            increment = increment_queue.get()
            # Process the increment
            redis_conn.incrby('counter', increment)
            print(f"Processed increment: {increment}")
            # Indicating that the item has been processed
            increment_queue.task_done()

"""Start the background thread."""
thread = threading.Thread(target=consumer, daemon=True)
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/click', methods=['POST'])
def click():
    # Enqueue an increment action
    increment_queue.put(1)
    return jsonify({'message': 'Increment queued'}), 200

@app.route('/counter', methods=['GET'])
def get_counter():
    # Return the most up-to-date counter value from Redis
    current_counter = fetch_db_value()
    return jsonify({'counter': current_counter}), 200

if __name__ == '__main__':
    # Runnign the Flask app
    application.run(debug=True, use_reloader=False)
