import matplotlib.pyplot as plt
import numpy as np
import queue

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
        print(process_sorted_list[i].arrival_time,
              process_sorted_list[i].burst_time, process_sorted_list[i].priority, process_sorted_list[i].start_time, process_sorted_list[i].finish_time)
            
    
    current_time =0
    PriorityQueue()

    for i in range (0,num_process):
        process_sorted_list[i].start_time = process_sorted_list[i].arrival_time+context_switching
        process_sorted_list[i].finish_time = process_sorted_list[i].start_time + process_sorted_list[i].burst_time






    





class Process:
    def __init__(self, idd,arrival_time, burst_time,priority,start_time,finish_time):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.finish_time = finish_time
        self.start_time = start_time
        self.idd = idd





HPF("os_project/output.txt",0)



