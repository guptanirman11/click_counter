# Project Cloud Clicker  
This project is a demonstration of CI/CD implementation for deploying a cloud-hosted Flask application with a global click counter feature, ensuring proper access control security and logging of counter clicks. This application also provides an option for live updates and incorporates free tier services from AWS to incorporate scalability and agility.

## Salient Features
* This project weighs in on two divergent approaches to this project to produce a website that allows multiple users to click and store the counts of their clicks. This counter is global (shared among all users throughout the lifetime of the deployment). Multiple users can access the website at the same time, who can all update the counter.
* Live updates have been implemented, in a judicious manner.
* The application runs on every code commit to this repository which is a part of a CI/CD pipeline connecting it to a secure cloud infrastructure with multiple user-roles and a record of metrics/logs. 

## User Guide 
The following are the key elements of this project:
* The final product is this website 


## Introduction
The project focuses on developing a scalable application architecture to handle write-heavy operations, particularly prioritizing click storage over immediate display updates. To achieve this, I explored and implemented two different approaches, each with its own architectural design considerations and trade-offs. The architecture is deployed on AWS, leveraging services like EC2 and Elasticache, with a streamlined CI/CD pipeline using AWS CodePipeline and robust monitoring through CloudWatch.

## Backend Approaches Explored
* Approach 1: Global Variable with Database Sync
This approach involves using a thread-safe operation (lock as supported in Python) on a global variable (using Singleton Pattern) to track clicks, with eventual synchronization with the database. 

* Approach 2: Producer-Consumer Model with Queue
Here, a thread-safe queue is employed to store click requests from users, with a dedicated pull worker responsible for fetching and updating the database. Here the producers are the users whereas consumer is the background thread. Here we will be updating the delta to counter in the RedisCache.

**I decided to use the later approach as blocking a resource which would have been the global counter in the first case is not the most optimal -- with locks the bottleneck and performance issues will arise as the other threads and requests will keep on spinnind and try to register their count.**

## Live Updates
Live updates are implemented with a periodic API call to the backend service every 5 seconds, balancing real-time updates with performance considerations to avoid unnecessary API calls. This could be changed eventually depending on the tradeoff between frequency of live updates required versus the number of API requests the system can handle.

## Consistency Management
I decided to adopt an eventual consistency model to handle high workloads without introducing significant latency. While strong consistency ensures immediate updates, eventual consistency ensures that all inputs are eventually processed, optimizing performance under heavy load.

## Database Choice
The decision to use a cache database like Redis or Elasticache was made based on performance, availability, and scalability requirements. The cache database efficiently handles high write and fetch loads, ensuring concurrent safety.

## AWS Architecture
The application is deployed on AWS using EC2 instances and Elasticache for caching. The choice of EC2 over a Lambda Function was driven by the need for background thread execution. Automation of cloud infrastructure setup was achieved, with CI/CD pipeline integration through AWS CodePipeline and CodeDeploy for streamlined deployment. I scripted an `appspec.yml` file which utilises bach scripts inside `code_deploy_scripts`. 

AWS CloudWatch is utilized for comprehensive monitoring, including reporting custom metric data via Boto3 to track the count of clicks. You can locate it under the "MyApplication" namespace with the customised metric name "Clicks." This provides insights into the frequency of clicks, enabling analysis through various options such as total counts, averages, and sum counts over time. Graphical representation typically updates every 5 minutes, aligning with intervals on the x-axis. Multiple other default metrics can also be viewed.

Using the IAM User functionality on AWS, I created the two 'roles' for access -- that of `OWNER` and `AUDITOR`. The credentials for accessing the AWS Management Console for each role are submitted in a `.zip` folder via email. The OWNER role has full access to all administrator permissions and can make changes to the architecture, besides accessing metrics and logs. The AUDITOR role can only access metrics or logs pertaining to the database, the CloudWatch, as well as the code deployment infrastructure. Upon making the first log-in by using the IAM account credentials (log-in URL, username, and password shared), the users will be prompted to reset the password to one of their own.

## Discussion of Access Control Security 

## Scope for Improvement
To enhance security, HTTPS can be implemented using a registered Domain Name system, though cost considerations influenced the decision for time being. Load balancing and scaling strategies can be employed to handle increasing server demands, alongside optimizations like increasing pull workers for faster queue processing (however, one drawback for this strategy might be that we might have to use multi-threading appraoches for avoiding race conditions). Integration of SQS instead of a custom thread-safe queue can further improve scalability and efficiency.

## Conclusion
The architectural design and implementation of the project aim to strike a balance between scalability, performance, and cost-effectiveness. By leveraging AWS services, employing efficient design patterns, and considering future scalability needs, the system is well-equipped to handle write-heavy workloads while maintaining optimal performance and reliability.

## Requirements

