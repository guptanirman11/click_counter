# Project Cloud Clicker  

## Business Requirement
A click counter application to map the number of clicks made by various users (including themselves) may or may not be accessing the application at the same time.

## System Requirements
### Functional Requirements
- A button that user can click.
- A counter that shows the total number of times the button has been clicked.
- Application should be deployed on cloud infrastructure with a CI/CD pipeline to automate application deployment process.
- The cloud infrastructure should have appropriate access control security. It should log the metrics to get frequency of the counter clicks.

### Non-Functional Requirements
- The project focuses on developing a scalable application architecture with increasing number of users to handle write-heavy operations.
- We implement the live updates (counter for one user updates as another person clicks it), hence, prioritizing click registration over immediate display updates.

### High Level Architecture
![image](https://github.com/guptanirman11/click_counter/assets/114794173/42433460-4401-482d-8200-e3a59b76f0e0)




## Extra Features
* This project weighs in on two divergent approaches to this project to produce a website that allows multiple users to click and store the counts of their clicks. This counter is global (shared among all users throughout the lifetime of the deployment). Multiple users can access the website at the same time, who can all update the counter.
* Live updates have been implemented, in a judicious manner.
* The application runs on every code commit to this repository which is a part of a CI/CD pipeline connecting it to a secure cloud infrastructure with multiple user-roles and a record of metrics/logs.
* Logs from the Flask application are documented to allow for debugging, testing, and performance monitoring.
* API Gateway to manage the API calls and securing them with HTTPS.


## User Guide 
The following are the key elements of this project (and repository):
* The final product is **[this website](http://3.89.220.49:5000)** which is called the `Cloud Clicker` -- a click counter housed on a cloud infrastructure (link: [http://3.89.220.49:5000](http://3.89.220.49:5000)).
*  The [`app`](https://github.com/guptanirman11/click_counter/tree/main/app) directory on this repository contains the backend and frontend files:
      * [`application.py`](https://github.com/guptanirman11/click_counter/blob/main/app/application.py): the backend framework listening to the API calls, also makes CloudWatch API calls to log metrics
      * [`worker.py`](https://github.com/guptanirman11/click_counter/blob/main/app/worker.py): describes the Pull Worker class able to connect to the cache and methods associated
      * [`db.py`](https://github.com/guptanirman11/click_counter/blob/main/app/db.py): describe the Cache connection and have methods associated with it
      * [`templates`](https://github.com/guptanirman11/click_counter/tree/main/app/templates) and [`static`](https://github.com/guptanirman11/click_counter/tree/main/app/static) directories: [`.html`](https://github.com/guptanirman11/click_counter/blob/main/app/templates/index.html), [`.css`](https://github.com/guptanirman11/click_counter/blob/main/app/static/styles.css), and [`.js`](https://github.com/guptanirman11/click_counter/blob/main/app/static/script.js) files required for rendering front-end
      * [`logs`](https://github.com/guptanirman11/click_counter/tree/main/app/logs) directory: [`access.log`](https://github.com/guptanirman11/click_counter/blob/main/app/logs/access.log) and [`error.log`](https://github.com/guptanirman11/click_counter/blob/main/app/logs/error.log) files documenting Flask application logs
      * [`singleton.py`](https://github.com/guptanirman11/click_counter/blob/main/app/singleton.py): singleton global counter approach for reference 
      * [`requirements.txt`](https://github.com/guptanirman11/click_counter/blob/main/app/requirements.txt): containing information regarding all the requirements and subsystems for reproducing this system
* The [`appspec.yml`](https://github.com/guptanirman11/click_counter/blob/main/appspec.yml) file which utilises bach scripts inside [`code_deploy_scripts`](https://github.com/guptanirman11/click_counter/tree/main/code_deploy_scripts) directory to automate the CI/CD pipelines and to give instructions for the deployment process. These files install dependencies, and run the Flask service using [`app.service`](https://github.com/guptanirman11/click_counter/blob/main/code_deploy_scripts/app.service) file. 
* [`cloud_setup/cloud_setup.py`](https://github.com/guptanirman11/click_counter/blob/main/cloud_setup/cloud_setup.py): cloud infrastructure (creating AWS security group, EC2 instance, Cache)
* [`test_app/test_application.py`](https://github.com/guptanirman11/click_counter/blob/main/app/test_application.py): unit test-cases for API calls, final sanitary checks ran before deploying on AWS


Below, I discuss some of these elements in depth, as well as detail some discussion on some of my choices as well as the future scope of this project.

## Steps Taken
To achieve the functional and non-functional requirements of the project, I explored and implemented two different backend design approaches, each with its own architectural design considerations and trade-offs. The architecture is deployed on AWS, leveraging services like EC2 and ElastiCache, API Gateway for GET and POST HTTPS requests with a streamlined CI/CD pipeline using AWS CodePipeline and CodeDeploy from GitHub as well as robust monitoring through CloudWatch.

## The Two Backend Approaches Explored
* _**Approach 1: Singleton Design Principle with Database/Cache Sync**_:
This approach involves using a thread-safe operation (lock as supported in Python) on a global variable Counter (A Singleton Class Object) to track clicks, with eventual synchronization with the Database/Cache.

<ins>Pros</ins>:
1) A Global Counter maintaining consistency of Counter for all the users.
2) Global access of the class (attributes and associated methods).

<ins>Cons</ins>:
1) The Critical Section is the Counter object which is the main resource.
2) Clicking actions and database updates are done synchronously.
3) As it is a write-heavy system, it would not be able to register all the counter clicks as efficently as expected. **With the lock the bottleneck and performance issues will arise as the other threads and requests will keep on spinning and try to register their count.**

* _**Approach 2: Producer-Consumer Model with Queue**_:
Here, a thread-safe queue is employed to store click requests from users, with a dedicated pull worker responsible for fetching and updating the database. Here the producers are the users whereas consumer is the background thread (A Pull Worker) which fetches the value from the queue (until the users are active or my queue in not empty). Here we will be updating the counter with delta in the RedisCache.

<ins>Pros:</ins>
1) Decouples clicking actions from database updates for improved responsiveness i.e. Asynchronous Processing.
2) We can maintain data integrity through re-queuing failed updates, enhancing reliability.
3) The queue also acts as a buffer to manage traffic bursts and scales by adding more consumers.

<ins>Cons</ins>:
1) Latency in Data Visibility as updates to the database are delayed.
2) Requires strategies to prevent unbounded growth of queue under high load, adding complexity.

**I decided to use the latter approach as blocking a resource which would have been the global counter in the first case is not optimal.**

## Live Updates
Live updates are implemented with a periodic API call to the backend service every 5 seconds, balancing real-time updates with performance considerations to avoid unnecessary API calls. This could be changed eventually depending on the tradeoff between frequency of live updates required versus the number of API requests the system can handle.

## Consistency Management
I decided to adopt an eventual consistency model to handle high workloads without introducing significant latency. While strong consistency ensures immediate updates, eventual consistency ensures that all inputs are eventually processed, optimizing performance under heavy load.

## Database/Cache Choice
The decision to use a cache database like ElastiCache was made based on performance, availability, and scalability requirements. The cache database efficiently handles high write and fetch loads, ensuring concurrent thread safety.
### Key-Value Schema
* Key: counter
* Value: An integer value that starts at 0 and increments with each click.


## AWS Architecture
The application is deployed on AWS using EC2 instances and ache for caching. The choice of EC2 over a Lambda Function was driven by the need for background thread execution. Automation of cloud infrastructure setup was achieved, with CI/CD pipeline integration through AWS CodePipeline and CodeDeploy for streamlined deployment. I scripted an [`appspec.yml`](https://github.com/guptanirman11/click_counter/blob/main/appspec.yml) file which utilises bach scripts inside [`code_deploy_scripts`](https://github.com/guptanirman11/click_counter/tree/main/code_deploy_scripts) to set up the pipeline. 

I have utilised APIGateway which acts as a powerful and secure front door to the backend service. It makes the API calls secure and make the application scale as the incoming traffic increases.

AWS CloudWatch is utilized for comprehensive monitoring, including reporting custom metric data via Boto3 to track the count of clicks. You can locate it under the "MyApplication" namespace with the customised metric name "Clicks". This provides insights into the frequency of clicks, enabling analysis through various options such as total counts, averages, and sum counts over time. Graphical representation typically updates every 5 minutes, aligning with intervals on the x-axis. Multiple other default metrics can also be viewed.

![image](https://github.com/guptanirman11/click_counter/assets/114794173/ccf5d090-ee61-43d4-aa47-aab771113ded)


Using the IAM User functionality on AWS, I created the two 'roles' for access -- that of `OWNER` and `AUDITOR`. The credentials for accessing the AWS Management Console for each role have been submitted in a `.zip` folder via email. The `OWNER` role has full access to all administrator permissions and can make changes to the architecture, besides accessing metrics and logs. The `AUDITOR` role can only access metrics or logs pertaining to the database, the CloudWatch, as well as the code deployment infrastructure. Upon making the first log-in by using the IAM account credentials (log-in URL, username, and password shared), the users will be prompted to reset the password to one of their own.

## API Endpoints
1) **Home Page**
* Endpoint: `/`
* Method: `GET`
* Description: Renders the homepage of the click counter application.
* Example Request: `curl http://3.89.220.49:5000/`

2) **Click**
* Endpoint: `/click`
* Method: `POST`
* Description:  Increments the counter by one. This endpoint is called every time a click is registered.
* Example Request: `curl'https://4ifqmulwvl.execute-api.us-east-1.amazonaws.com/testing/click` (API Gateway Endpoint) 
* Response :
       ```{
  "message": "Increment queued"
          }```

3) **Home Page**
* Endpoint: `/counter`
* Method: GET
* Description: Fetches the current value of the counter from ElasticCache.
* Example Request: `curl 'https://4ifqmulwvl.execute-api.us-east-1.amazonaws.com/testing/counter` (API Gateway Endpoint) 
* Response :
     ```{"counter": "42"}```

## Discussion of Access Control Security 
I considered a few aspects pertaining to access control security in setting up this application:
* **Authorization**: Enforcing fine-grained access control policies to determine what actions users or services are allowed to perform within the application 
(manifested through authorization mechanisms based on groups, roles, permissions, and attributes associated with the entities such as `OWNER` or `AUDITOR`) and leveraging the Principle of Least Privilege.
* **Secure Communication**: By leveraging the appropriate security groups and IAM roles associated with AWS services, it has been ensured that some restriction is placed on the ports to listen to.
* **Multi-Factor Authentication**: Implemented to allow checks on users accessing the system. 
* **Monitoring and Logging**: Implement logging and monitoring capabilities to track access to resources.


## Scope for Improvement
### Security:
* **Implementing HTTPS**: Secures client-server communications, protecting against eavesdropping and tampering for the static website as well.
### Reliability:
* **Implementing Robust Testing**: Early identification and correction of flaws through integration testing in the CI phase can help boost reliability.
* **Data Handling and Segregation**: Segregating data tasks can enhance integrity and reduce errors, improving reliability.
### Availability:
* **Utilizing Load Balancing**: Distributing traffic to prevent bottlenecks, load balancing would help enhance application availability.
* **Incorporating Adaptive Live Updates**: By aligning the provision of live updates 'elastically' through an adaptive approach, we can balance load based on user activity, maintaining system responsiveness and availability.
### Performance:
* **Scaling Horizontally**: Adding resources to meet demand without straining infrastructure, boosting performance.
* **Increasing Pull Workers**: More workers processing queue items can help increase throughput and performance.
* **Integrating AWS SQS**: Using SQS as the architecture becomes distributed i.e. operating across multiple servers, whereas current queue is an in-memory, thread-safe queue designed for inter-thread communication within the same application process.
* **Utilizing Work Stealing**: Optimizing resource use by reallocating tasks among workers as well we can enhance performance.
* **Further Considering Serverless Architecture**: An alternative infrastructure choice can be explored further depending on priorities, to check if it can help us dynamically allocate resources based on demand through the serverless setup, ensuring efficient performance scaling.

## Conclusion
The architectural design and implementation of the project aim to strike a balance between scalability, performance, and cost-effectiveness. By leveraging AWS services, employing efficient design patterns, and considering future scalability needs, the system is well-equipped to handle write-heavy workloads while maintaining optimal performance and reliability.

## Requirements
* boto3==1.34.67
* botocore==1.34.67
* click==8.1.7
* Flask==3.0.2
* Flask-Cors==4.0.0
* Flask-SocketIO==5.3.6
* gunicorn==21.2.0
* redis==5.0.3
* s3transfer==0.10.1
