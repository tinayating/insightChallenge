Author: Yating Tian

Time: Apr 5th, 2018

**Approach:**

- Create a hashmap to store current active session. Key: ip; Value: [start_time, end_time, num_request, counter]
  - star_time: first request time
  - end_time: last request time
  - num_request: number of requests made by the users
  - counter: a counter indicates the latest row num in the log file
- Each time, read a line from the log file.
  - First, get current time and iterate through the map to check whether the duration (current_time - end_time) is greater than the inactivity_period. 
    - If yes, means the session is over -> add those sessions into a output list,  sort them ascendingly based on the counter -> write the logs in  output list to the output file. Then, drop those logs from the hashmap
  - Second, add current log to the hashmap
    - If current log not exists in the hashmap, add
    - If exists, update end_time to current_time, num_request + 1
- End of the file, print all the logs in the hashmap based on the order in the input file


**Dependencies:** None


**Run instructions:**

cd to _insight_testsuite_ folder, run the following:

```
insight_testsuite~$ ./run.sh 
```