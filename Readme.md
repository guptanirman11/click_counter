## Architectural Design
For the Backend logic of Counter, two possible design patterns were Observer and Singleton. However, for observer the users are notfied at an event and keep a track of users which is not required for Counter, whereas Singleton pattern will make sure that only one instance of Counter is created and used

## Strong V/S Eventual Consisteny
If we go for Strong Cinsistncy then the Workload would be higher and their will be latency to update value when there are 100s of requests. Eventual COnsistency will help us make sure that at the end all the inputs are being monitored and stored properly.

## Database choice
I have decided to use a cache db such as redis or Elasticcache in AWS. I choose a cache db due to the performance, availability and scalability. As the number of writes and fetches are high as one user can click multiple times so in order to make it concurrent safe as well.


### Things I have tried
I am trying two version 
1) Having a thread-safe operation to global variable and then eventually making it consistent across users from db
2) Having a thread safe queue where each user requests are stored and a pull worker will keep ontry to fetch the new values if it is not empty. This mimics the producer consumer model where producer does not process if queue is empty.

### aws architecture
Used ec2, elastic cache for deploying the website. As there was a need for background thread running I decided to use ec2 over lambda function. Though we can mimic the behaviour by using a sqs queue to create event of triggering the value update in redis cache but due to time constraint I decided to go with EC2 instance. I created a file to automate the cloud infrastructure process and used boto3 for the same. After that i will add a CI/CD pipeline connected to public repo and attach cloudwatch logging system for the same.
