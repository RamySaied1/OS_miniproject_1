from Process import Process
import numpy as np
#process number, arrival time, burst time and priority.
def RR(processes,context_switching_time,quantum):
    queue = list()
    processes.sort(key=lambda elem: (elem.arrival_time,elem.idd))
    #for i in processes:
    #    print(i.idd,i.arrival_time,i.burst_time,i.priority)
    
    finish = 0
    time = processes[0].arrival_time
    #this variable tell form where i start to insert new processes based on arrival time to avoid inserting low arrival time porcess again
    toArrive=1
    queue.append(processes[0])
    finish_time={}
    #this valriable is use to there will be contextswitch overhead or not and it's intialied with -1 to incluede overhed of first process as TA said
    last_proccess_id = -1

    # save all running times corresponding to its ids for chart graph
    runing_times = {} 
    while(finish!=len(processes)):
        #run -> insert in queue -> put run porecces in last of queue
        # time before running any process
        if(last_proccess_id!=queue[0].idd):
            time += context_switching_time
        
        #run
        curr_porccess_finsihed = quantum >= queue[0].burst_time
        #save start time and end time 
        startTime=time
        #save processid  note: even if process removed new process will come has different id so there is overhead like @ beggining (TA)
        last_proccess_id = queue[0].idd 
        if(curr_porccess_finsihed):
            time += queue[0].burst_time
            finish_time[queue[0].idd]=time            
            queue.pop(0)
            finish+=1
        else: 
            time+=quantum
            queue[0].burst_time-=quantum
        endTime=time
        #save running time into dictinary
        runing_times[(startTime,endTime)]= last_proccess_id
        
        #if queue is empty and no one will arrive at current time i don't have to walkthrough all timesteps so i can set next time step to
        #smallest arrival time
        if(toArrive<len(processes) and not len(queue) and time < processes[toArrive].arrival_time):
            time = processes[toArrive].arrival_time 

        #insert arrived processes in queue
        new_processes_num=0
        for i in range(toArrive,len(processes)):
            if(processes[i].arrival_time<=time):
                queue.append(processes[i])  
                new_processes_num+=1
            else: break
        toArrive += new_processes_num
       
        #if proccess not removed in queue put it at end of queueu
        if(not curr_porccess_finsihed):
            queue.append(queue.pop(0))
    
    #Waiting,Turnaround,WeightedTurnaround
    metric = np.zeros((len(processes),4)).astype(np.float)

    #filling 
    for i in range(len(processes)):
        metric[i,0] = processes[i].idd
        metric[i,2] = finish_time[processes[i].idd]-processes[i].arrival_time # TAT = finish - arrival
        metric[i,1] = metric[i,2] = processes[i].burst_time # Wating = TAT - burst_time
        metric[i,3] = 1.*metric[i,2] / processes[i].burst_time # WTAT = TAT/burst_time
   

    #print (metric,runing_times)
    return metric,runing_times
    