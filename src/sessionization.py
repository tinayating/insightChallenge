from datetime import datetime, date, time
import sys

def read_log(header_dict, line, all_log, inactivity_period, outputFile, f_open, counter):
    """
    :param header: the header of log file
    :param line: each line in the log file
    :param all_log: a dictionary of all logs
    :return: not applicable
    """
    # construct a time stamp
    item = line.split(",")
    d_list = item[header_dict['date']].split('-')
    t_list = item[header_dict['time']].split(':')
    d = date(int(d_list[0]),int(d_list[1]),int(d_list[2]))
    t = time(int(t_list[0]),int(t_list[1]),int(t_list[2]))
    timestamp = datetime.combine(d,t)

    # for loop all the timestamp in all_log
    delete_list = []
    output_list = [] # a list used to store the temporary output
    for k,v in all_log.items():
        if (timestamp - v[1]).seconds > int(inactivity_period): #v[1] is the last request time
            # write to output
            output_list.append((",".join([k,str(v[0]),str(v[1]),str((v[1]-v[0]).seconds+1),str(v[2])])+"\n",v[3])) # store a tuple (output, counter)
            # add logs to delete_list, remove items in the list later
            delete_list.append(k)
			
    for key in delete_list:
        all_log.pop(key)
		
    output_list = sorted(output_list, key = lambda x:x[1])
	
    for output_line in output_list:
        f_open.write(output_line[0])
    # create a log dict. key: userip, value[start_time, endtime, num_request, counter]
    if item[header_dict['ip']] not in all_log:
        all_log[item[header_dict['ip']]] = [timestamp, timestamp, 1, counter]

    else:
        last_log = all_log[item[header_dict['ip']]]
        last_log[1] = timestamp # update the value of end_time
        last_log[2] += 1 # update the value of count


if __name__ == '__main__':
    outputFile = sys.argv[3]
    with open(sys.argv[2]) as f:
        inactivity_period = f.readline().strip('\n')
    with open(sys.argv[1]) as f:
        counter = 0
        header_dict = {}
        all_log = {}
        with open(outputFile,'w') as f_open:
            for line in f.readlines():
                line = line.strip('\n')
                print(line)
                if counter == 0:
                    header = line
                    header = header.split(",")
                    # put the header into a dict for reference
                    for i in range(len(header)):
                        header_dict[header[i]] = i
                else:
                    read_log(header_dict, line, all_log, inactivity_period, outputFile, f_open, counter)
                counter += 1
        # end of the file, print all the logs in all_log
            output_list = []
            for k,v in all_log.items():
                output_list.append((",".join([k,str(v[0]),str(v[1]),str((v[1]-v[0]).seconds+1),str(v[2])])+"\n",v[3])) #v[1] - v[0] returns a timedelta
            output_list = sorted(output_list, key = lambda x:x[1])
            for output_line in output_list:
                f_open.write(output_line[0])