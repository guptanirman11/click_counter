# from flask import Flask, jsonify
# from flask_cors import CORS
# import sqlite3
# import threading
# import time


# def fetch_db_value():
#      with sqlite3.connect('counter.db') as conn:
#             cursor = conn.cursor()
#             cursor.execute('SELECT count FROM counts WHERE id = 1')
#             row = cursor.fetchone()
#             return row[0] if row else 0
     

# # Singleton Counter class to manage the global counter state
# class Counter:
#     _instance = None
#     _lock = threading.Lock()

#     def __new__(cls):
#         with cls._lock:
#             if cls._instance is None:
#                 cls._instance = super().__new__(cls)
#                 cls._instance.value = fetch_db_value()
#         return cls._instance

#     def increment(self):
#         with self._lock:
#             self.value += 1

#     def get_value(self):
#         return self.value
        

# app = Flask(__name__)
# CORS(app)
# counter = Counter()

# def init_db():
#     with sqlite3.connect('counter.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute('CREATE TABLE IF NOT EXISTS counts (id INTEGER PRIMARY KEY, count INTEGER)')
#         # cursor.execute('INSERT INTO counts (id, count) SELECT 1, 0 WHERE NOT EXISTS (SELECT 1 FROM counts WHERE id = 1)')
#         conn.commit()

# def sync_counter_to_db():
#     with sqlite3.connect('counter.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute('UPDATE counts SET count = ? WHERE id = 1', (counter.value,))
#         conn.commit()

# # Background thread to periodically sync the counter value to the database
# def background_sync():
#     while True:
#         time.sleep(10)
#         print(counter.value, threading.current_thread)
#         print("here")
#         sync_counter_to_db()




# # RESTful API Endpoints using Flask
# # Click endpoint to handle user clicks on the button
# @app.route('/click', methods=['POST'])
# def click():
#     counter.increment()
#     return jsonify({'counter': counter.get_value()}), 200
# # Counter endpoint to retrieve the current value of the counter

# @app.route('/counter', methods=['GET'])
# def get_counter():
    
#     return jsonify({'counter': fetch_db_value()}), 200


# if __name__ == '__main__':
   
#     thread = threading.Thread(target=background_sync, daemon=True)
#     init_db()
#     thread.start()
    
#     app.run(debug=True, use_reloader=False)


from flask import Flask, jsonify
from flask_cors import CORS
import redis
import threading
import time

# Initialize Redis connection
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def fetch_db_value():
    # Use Redis GET. If the key doesn't exist, initialize it to 0.
    value = redis_conn.get('counter') or 0
    print(f'fetched: {value}')
    return int(value)

# Singleton Counter class to manage the global counter state
class Counter:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.value = fetch_db_value()
        return cls._instance

    def increment(self):
        with self._lock:
            self.value += 1
            redis_conn.set('counter', self.value)

    def get_value(self):
        return self.value

app = Flask(__name__)
CORS(app)
counter = Counter()

# Background thread to periodically sync the counter value to the database
# With Redis being more performant, you might not need this, but it's here for consistency
def background_sync():
    while True:
        time.sleep(10)
        print(f'counter value: {counter.get_value()}')

# RESTful API Endpoints using Flask
@app.route('/click', methods=['POST'])
def click():
    counter.increment()
    return jsonify({'counter': counter.get_value()}), 200

@app.route('/counter', methods=['GET'])
def get_counter():
    return jsonify({'counter': fetch_db_value()}), 200

if __name__ == '__main__':
    thread = threading.Thread(target=background_sync, daemon=True)
    thread.start()
    app.run(debug=True, use_reloader=False)
