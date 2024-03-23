# Project Cloud Clicker  
This project is a demonstration of CI/CD implementation for deploying a cloud-hosted Flask application with a global click counter feature, ensuring proper access control security and logging of counter clicks. This application also provides an option for live updates and incorporates free tier services from AWS to incorporate scalability and agility.

## Salient Features
* This project weighs in on two divergent approaches to this project to produce a website that allows multiple users to click and store the counts of their clicks. This counter is global (shared among all users throughout the lifetime of the deployment). Multiple users can access the website at the same time, who can all update the counter.
* Live updates have been implemented, in a judicious manner.
* The application runs on every code commit to this repository which is a part of a CI/CD pipeline connecting it to a secure cloud infrastructure with multiple user-roles and a record of metrics/logs.
* Logs from the Flask application are documented to allow for debugging, testing, and performance monitoring.

## User Guide 
The following are the key elements of this project (and repository):
* The final product is **[this website](http://3.89.220.49:5000)** which is called the `Cloud Clicker` -- a click counter housed on a cloud infrastructure (link: [http://3.89.220.49:5000](http://3.89.220.49:5000)).
*  The [`app`](https://github.com/guptanirman11/click_counter/tree/main/app) directory on this repository contains the backend and frontend files:
      * [`application.py`](https://github.com/guptanirman11/click_counter/blob/main/app/application.py): the backend framework listening to the API calls, also makes CloudWatch API calls to log metrics 
      * [`cloud_setup.py`](https://github.com/guptanirman11/click_counter/blob/main/app/cloud_setup.py): cloud infrastructure (creating AWS security group, EC2 instance, ElastiCache)
      * [`templates`](https://github.com/guptanirman11/click_counter/tree/main/app/templates) and [`static`](https://github.com/guptanirman11/click_counter/tree/main/app/static) directories: [`.html`](https://github.com/guptanirman11/click_counter/blob/main/app/templates/index.html), [`.css`](https://github.com/guptanirman11/click_counter/blob/main/app/static/styles.css), and [`.js`](https://github.com/guptanirman11/click_counter/blob/main/app/static/script.js) files required for rendering front-end
      * [`logs`](https://github.com/guptanirman11/click_counter/tree/main/app/logs) directory: [`access.log`](https://github.com/guptanirman11/click_counter/blob/main/app/logs/access.log) and [`error.log`](https://github.com/guptanirman11/click_counter/blob/main/app/logs/error.log) files documenting Flask application logs
      * [`singleton.py`](https://github.com/guptanirman11/click_counter/blob/main/app/singleton.py): singleton global counter approach for reference 
      * [`requirements.txt`](https://github.com/guptanirman11/click_counter/blob/main/app/requirements.txt): containing information regarding all the requirements and subsystems for reproducing this system
* The [`appspec.yml`](https://github.com/guptanirman11/click_counter/blob/main/appspec.yml) file which utilises bach scripts inside [`code_deploy_scripts`](https://github.com/guptanirman11/click_counter/tree/main/code_deploy_scripts) directory to automate the CI/CD pipelines and to give instructions for the deployment process.
      * These files install dependencies, and run the Flask service using [`app.service`](https://github.com/guptanirman11/click_counter/blob/main/code_deploy_scripts/app.service) file. 

Below, I discuss some of these elements in depth, as well as detail some discussion on some of my choices as well as the future scope of this project.

## Introduction
The project focuses on developing a scalable application architecture to handle write-heavy operations, particularly prioritizing click storage over immediate display updates. To achieve this, I explored and implemented two different approaches, each with its own architectural design considerations and trade-offs. The architecture is deployed on AWS, leveraging services like EC2 and Elasticache, with a streamlined CI/CD pipeline using AWS CodePipeline and robust monitoring through CloudWatch.

## Backend Approaches Explored
* _**Approach 1: Global Variable with Database Sync**_:
This approach involves using a thread-safe operation (lock as supported in Python) on a global variable (using Singleton Pattern) to track clicks, with eventual synchronization with the database. 

* _**Approach 2: Producer-Consumer Model with Queue**_:
Here, a thread-safe queue is employed to store click requests from users, with a dedicated pull worker responsible for fetching and updating the database. Here the producers are the users whereas consumer is the background thread. Here we will be updating the delta to counter in the RedisCache.

**I decided to use the later approach as blocking a resource which would have been the global counter in the first case is not the most optimal -- with locks the bottleneck and performance issues will arise as the other threads and requests will keep on spinnind and try to register their count.**

## Live Updates
Live updates are implemented with a periodic API call to the backend service every 5 seconds, balancing real-time updates with performance considerations to avoid unnecessary API calls. This could be changed eventually depending on the tradeoff between frequency of live updates required versus the number of API requests the system can handle.

## Consistency Management
I decided to adopt an eventual consistency model to handle high workloads without introducing significant latency. While strong consistency ensures immediate updates, eventual consistency ensures that all inputs are eventually processed, optimizing performance under heavy load.

## Database Choice
The decision to use a cache database like Redis or ElastiCache was made based on performance, availability, and scalability requirements. The cache database efficiently handles high write and fetch loads, ensuring concurrent safety.

## AWS Architecture
The application is deployed on AWS using EC2 instances and Elasticache for caching. The choice of EC2 over a Lambda Function was driven by the need for background thread execution. Automation of cloud infrastructure setup was achieved, with CI/CD pipeline integration through AWS CodePipeline and CodeDeploy for streamlined deployment. I scripted an [`appspec.yml`](https://github.com/guptanirman11/click_counter/blob/main/appspec.yml) file which utilises bach scripts inside [`code_deploy_scripts`](https://github.com/guptanirman11/click_counter/tree/main/code_deploy_scripts) to set up the pipeline. 

AWS CloudWatch is utilized for comprehensive monitoring, including reporting custom metric data via Boto3 to track the count of clicks. You can locate it under the "MyApplication" namespace with the customised metric name "Clicks". This provides insights into the frequency of clicks, enabling analysis through various options such as total counts, averages, and sum counts over time. Graphical representation typically updates every 5 minutes, aligning with intervals on the x-axis. Multiple other default metrics can also be viewed.

Using the IAM User functionality on AWS, I created the two 'roles' for access -- that of `OWNER` and `AUDITOR`. The credentials for accessing the AWS Management Console for each role have been submitted in a `.zip` folder via email. The `OWNER` role has full access to all administrator permissions and can make changes to the architecture, besides accessing metrics and logs. The `AUDITOR` role can only access metrics or logs pertaining to the database, the CloudWatch, as well as the code deployment infrastructure. Upon making the first log-in by using the IAM account credentials (log-in URL, username, and password shared), the users will be prompted to reset the password to one of their own.

## Discussion of Access Control Security 
I considered a few aspects pertaining to access control security in setting up this application:
* Authorization: Enforcing fine-grained access control policies to determine what actions users or services are allowed to perform within the application 
(manifested through authorization mechanisms based on groups, roles, permissions, and attributes associated with the entities such as `OWNER` or `AUDITOR`) and leveraging the Principle of Least Privilege.
* Secure Communication: By leveraging the appropriate security groups and IAM roles associated with AWS services, it has been ensured that some restriction is placed on the ports to listen to.
* Multi-Factor Authentication: Implemented to allow checks on users accessing the system. 
* Monitoring and Logging: Implement logging and monitoring capabilities to track access to resources.


## Scope for Improvement
To enhance security, HTTPS can be implemented using a registered Domain Name System, though cost considerations influenced the decision for time being. Load balancing and scaling strategies can be employed to handle increasing server demands, alongside optimizations like increasing pull workers for faster queue processing (however, one drawback for this strategy might be that we might have to use multi-threading appraoches for avoiding race conditions). Integration of SQS instead of a custom thread-safe queue can further improve scalability and efficiency. Further testing can also be implemented to make the system more robust.

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
