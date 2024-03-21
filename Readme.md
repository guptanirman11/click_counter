## Architectural Design
For the Backend logic of Counter, two possible design patterns were Observer and Singleton. However, for observer the users are notfied at an event and keep a track of users which is not required for Counter, whereas Singletin pattern will make sure that only one instance of Counter is created and used

## Strong V/S Eventual Consisteny
If we go for Strong Cinsistncy then the Workload would be higher and their will be latency to update value when there are 100s of requests. Eventual COnsistency will help us make sure that at the end all the inputs are being monitored and stored properly.

## Database choice
I have decided to use a cache db such as redis or Elasticcache in AWS. I choose a cache db due to the performance, availability and scalability. As the number of writes and fetches are high as one user can click multiple times so in order to make it concurrent safe as well.


### Things I have tried
I am trying two version 
1) Having a thread-safe operation to global variable and then eventually making it consistent across users from db
2) Having a thread safe queue where each user requests 