# from flask import Flask, jsonify, render_template
# from flask_cors import CORS
# from worker import PullWorker
# from db import RedisClient
# import redis
# import time
# from queue import Queue
# import boto3

# # Connecting with Cloudwatch to log the metrics
# cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

# app = Flask(__name__)
# application = app
# CORS(application)

# # Initializing Redis connection
# redis_conn = redis.StrictRedis(host='my-redis-cluster.0diz5e.ng.0001.use1.cache.amazonaws.com', port=6379, db=0, decode_responses=True)

# # Initializing a thread-safe queue for counter increment actions
# increment_queue = Queue()

# def fetch_db_value():
#     # fetching value from Redis
#     value = redis_conn.get('counter') or 0
#     print(f'fetched: {value}')
#     return int(value)

# """Starting the Worker"""
# worker = PullWorker(host='my-redis-cluster.0diz5e.ng.0001.use1.cache.amazonaws.com', port=6379, db=0, increment_queue=increment_queue)
# worker.start()

# '''Rendering the wesite isung rest api endpoint'''
# @app.route('/')
# def index():
#     return render_template('index.html')

# '''Post method called everytime a click is made'''
# @app.route('/click', methods=['POST'])
# def click():
#     # Enqueue an increment action
#     increment_queue.put(1)
#     print("Click Registered")
#     # Send custom metric data to CloudWatch
#     cloudwatch.put_metric_data(
#         Namespace='MyApplication',
#         MetricData=[
#             {
#                 'MetricName': 'Clicks',
#                 'Dimensions': [
#                     {
#                         'Name': 'Application',
#                         'Value': 'MyClickCounterApp'
#                     },
#                 ],
#                 'Unit': 'Count/Second',
#                 'Value': 1
#             },
#         ]
#     )
#     return jsonify({'message': 'Increment queued'}), 200

# '''Get method to fetch the Click Value aiding in implementing the live updates'''
# @app.route('/counter', methods=['GET'])
# def get_counter():
#     # Return the most up-to-date counter value from Redis
#     current_counter = fetch_db_value()
#     return jsonify({'counter': current_counter}), 200

# if __name__ == '__main__':
#     # Runnign the Flask app
#     application.run(debug=True, use_reloader=False)


# application.py
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from worker import PullWorker
from queue import Queue
import boto3
from db import RedisClient

class CloudClickerApplication:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

        self.redis_client = RedisClient()
        self.increment_queue = Queue()

        # Setup CloudWatch
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

        # Start worker
        self.worker = PullWorker(host='my-redis-cluster.0diz5e.ng.0001.use1.cache.amazonaws.com', port=6379, db=0, increment_queue=self.increment_queue)
        self.worker.start()

        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/click', methods=['POST'])
        def click():
            self.increment_queue.put(1)
            print("Click Registered")
            self.cloudwatch.put_metric_data(
                Namespace='MyApplication',
                MetricData=[{'MetricName': 'Clicks', 'Dimensions': [{'Name': 'Application', 'Value': 'MyClickCounterApp'}], 'Unit': 'Count/Second', 'Value': 1}]
            )
            return jsonify({'message': 'Increment queued'}), 200

        @self.app.route('/counter', methods=['GET'])
        def get_counter():
            current_counter = self.redis_client.fetch_db_value()
            return jsonify({'counter': current_counter}), 200

if __name__ == '__main__':
    cloud_clicker_application = CloudClickerApplication()
    cloud_clicker_application.app.run(debug=True, use_reloader=False)

# Expose the Flask application instance for Gunicorn
application = cloud_clicker_application.app
