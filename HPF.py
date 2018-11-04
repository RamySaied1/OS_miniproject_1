import matplotlib.pyplot as plt
from Process import Process
import numpy as np
import queue as Q
# assume lowest priority number is high priority
def HPF(input_file,context_switching):

    input = open(input_file, 'r')

    lines=input.readlines()
    process_list=[]
    num_process=int(lines[0])

    for i in range(0,num_process):
        line=lines[i+1].split()
        print(line)
        process_list.append(Process(int(line[0]),float(line[1]), float(line[2]), float(line[3]),0,0))
    
    process_sorted_list = sorted(process_list, key=lambda Process: (
        Process.arrival_time, Process.priority));

    for  i in range(0, num_process):
        print(process_sorted_list[i].idd,process_sorted_list[i].arrival_time,
              process_sorted_list[i].burst_time, process_sorted_list[i].priority, process_sorted_list[i].start_time, process_sorted_list[i].finish_time)
            
    
    current_time =0
    q = Q.PriorityQueue()
    result=[]

    while len(process_sorted_list)>0:
        if current_time <=process_sorted_list[0].arrival_time:
            current_time=process_sorted_list[0].arrival_time

        while (len(process_sorted_list) > 0) and(process_sorted_list[0].arrival_time <= current_time):
            q.put((process_sorted_list[0].priority,process_sorted_list[0]))
            process_sorted_list.pop(0)
    

        while not q.empty():
            priotity,process= q.get()
            process.start_time=current_time+context_switching
            process.finish_time=process.start_time+process.burst_time
            current_time=process.finish_time
            result.append(process)
            while (len(process_sorted_list) > 0) and(process_sorted_list[0].arrival_time <= current_time):
                q.put((process_sorted_list[0].priority, process_sorted_list[0]))
                process_sorted_list.pop(0)


    for i in range(0,len(result)):
        print(str(result[i].idd)+" "+str(result[i].start_time)+" "+str(result[i].finish_time)+" ")
    return result



result=HPF("./output.txt",0)
y  = []
start = []
width = []
for i in range(0,len(result)):
    y.append(result[i].idd)
    start.append(result[i].start_time)
    width.append(result[i].finish_time-result[i].start_time)
x1, x2, y1, y2 = plt.axis()
plt.axis((x1, x2, 0, len(result)))
plt.figure()
plt.barh(height=y, width=width , left=start,y=0,align="edge")
plt.show()





