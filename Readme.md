## Introduction
The project focuses on developing a scalable application architecture to handle write-heavy operations, particularly prioritizing click storage over immediate display updates. To achieve this, I explored and implemented two different approaches, each with its own architectural design considerations and trade-offs. The architecture is deployed on AWS, leveraging services like EC2 and Elasticache, with a streamlined CI/CD pipeline using AWS CodePipeline and robust monitoring through CloudWatch.

## BackendApproaches Explored
Approach 1: Global Variable with Database Sync
This approach involves using a thread-safe operation(lock as supported in Python) on a global variable(using Singleton Pattern) to track clicks, with eventual synchronization with the database. 

Approach 2: Producer-Consumer Model with Queue
Here, a thread-safe queue is employed to store click requests from users, with a dedicated pull worker responsible for fetching and updating the database. Here the producers are the users whereas consumer is the background thread. Here we will be updating the delta to counter in the RedisCache.

### I decided to use the later approach as blocking a resource which would have been the global counter in the first case is not the most optimal because with locks the bottleneck and performance issues will arise as the other threads and requests will keep on spinnind and try to register their count.

## Live Updates
Live updates are implemented with a periodic API call to the backend service every 5 seconds, balancing real-time updates with performance considerations to avoid unnecessary API calls. This could be changed eventually.

## Consistency Management
I decided to adopt an eventual consistency model to handle high workloads without introducing significant latency. While strong consistency ensures immediate updates, eventual consistency ensures that all inputs are eventually processed, optimizing performance under heavy load.

## Database Choice
The decision to use a cache database like Redis or Elasticache was made based on performance, availability, and scalability requirements. The cache database efficiently handles high write and fetch loads, ensuring concurrent safety.

## AWS Architecture
The application is deployed on AWS using EC2 instances and Elasticache for caching. The choice of EC2 over Lambda was driven by the need for background thread execution. Automation of cloud infrastructure setup was achieved, with CI/CD pipeline integration through AWS CodePipeline for streamlined deployment. I scripted an appspec.yml file which utilises bach scripts inside code_deploy_scripts. 

CloudWatch is utilized for comprehensive monitoring, including custom metric data reporting via Boto3 for Clicks. You could find it under "Namespace" MyApplication for Metric Name Clicks. This sends the frequency of the clicks which can be seen in the metrics and various options could be used to check total counts, avaergae, sum counts with time. It usually takes 5mins to show the clicks on the graph as it shows the graph when the next 5min time comes on x-axis.

Using the IAM User functionality on AWS, I created the two 'roles' -- that of OWNER and AUDITOR. The credentials for accessing the AWS Management Console for each role are housed here. The OWNER role has full access to all administrator permissions and can make changes to the architecture. The AUDITOR role can also access metrics pertaining to the database, the CloudWatch, and the code deployment infrastructure. 

## Scope for Improvement
To enhance security, HTTPS can be implemented using a registered Domain Name system, though cost considerations influenced the decision for time being. Load balancing and scaling strategies can be employed to handle increasing server demands, alongside optimizations like increasing pull workers for faster queue processing (however, one drawback for this strategy might be that we might have to use multi-threading appraoches for avoiding race conditions). Integration of SQS instead of a custom thread-safe queue can further improve scalability and efficiency.

## Conclusion
The architectural design and implementation of the project aim to strike a balance between scalability, performance, and cost-effectiveness. By leveraging AWS services, employing efficient design patterns, and considering future scalability needs, the system is well-equipped to handle write-heavy workloads while maintaining optimal performance and reliability.