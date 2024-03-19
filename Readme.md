## Architectural Design

For the Backend logic of Counter, two possible design patterns were Observer and Singleton. However, for observer the users are notfied at an event and keep a track of users which is not required for Counter, whereas Singletin pattern will make sure that only one instance of Counter is created and used

## Strong V/S Eventual Consisteny
If we go for Strong Cinsistncy then the Workload would be higher and their will be latency to update value whene there are 100s of requests. Eventual COnsistency will help us make sure that at the end all the inputs are being monitored and stored properly.