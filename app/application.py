from flask import Flask, jsonify, render_template
from flask_cors import CORS
from worker import PullWorker
from queue import Queue
import boto3
from DBUtils import RedisClient

# Class for Cloud Clicker Flask App
class CloudClickerApplication:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

        # Redis cache object from db.py
        self.redis_client = RedisClient()
        self.redis_client.reset_counter()
        self.increment_queue = Queue()
        

        # CloudWatch Setup
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

        # Pull worker object from worker.py
        self.worker = PullWorker(host='my-redis-cluster.0diz5e.ng.0001.use1.cache.amazonaws.com', port=6379, db=0, increment_queue=self.increment_queue)
        self.worker.start()

        self.setup_routes()

    # Method for API endpoints
    def setup_routes(self):
        # Renders the home page
        @self.app.route('/')
        def index():
            return render_template('index.html')

        # registers the click event and put in the queue
        @self.app.route('/click', methods=['POST'])
        def click():
            self.increment_queue.put(1)
            print("Click Registered")
            self.cloudwatch.put_metric_data(
                Namespace='MyApplication',
                MetricData=[{'MetricName': 'Clicks', 'Dimensions': [{'Name': 'Application', 'Value': 'MyClickCounterApp'}], 'Unit': 'Count/Second', 'Value': 1}]
            )
            return jsonify({'message': 'Increment queued'}), 200
        
        # responds to the Get call to fetch the updated value in Cache
        @self.app.route('/counter', methods=['GET'])
        def get_counter():
            current_counter = self.redis_client.fetch_db_value()
            return jsonify({'counter': current_counter}), 200

if __name__ == '__main__':
    cloud_clicker_application = CloudClickerApplication()
    cloud_clicker_application.app.run(debug=True, use_reloader=False)

# Exposing the Flask application instance for Gunicorn
application = cloud_clicker_application.app
