from Process import Process
import numpy as np
#process number, arrival time, burst time and priority.
def SNRT(processes,context_switching_time):
    quantum=10000.0
    for p in processes:
        quantum=min(p.burst_time,quantum)
   #assume scheduler check every value that less than minimum running tume process
    quantum/=2

    arrived = list()
    processes.sort(key=lambda elem: (elem.arrival_time,elem.idd))


    #this variable tell form where i start to insert new processes based on arrival time to avoid inserting low arrival time porcess again
    toArrive=0
    finish_time={}

    #this valriable is use to there will be contextswitch overhead or not and it's intialied with -1 to incluede overhed of first process as TA said
    last_proccess_id = -1

    #this variable tells which process in arrived list is currently running
    currently_running=0

    # save all running times corresponding to its ids for chart graph
    runing_times = {} 
   
    finish = 0
    time = 0.0
    while(finish!=len(processes)):
        #insert all arrived -> schedule ->run

        #if arrived is empty and no one will arrive at current time i don't have to walkthrough all timesteps so i can set next time step to
        #smallest arrival time
        if(toArrive<len(processes) and not len(arrived) and time < processes[toArrive].arrival_time):
            time = processes[toArrive].arrival_time 

        #insert arrived processes in arrived
        new_processes_num=0
        for i in range(toArrive,len(processes)):
            if(processes[i].arrival_time<=time):
                arrived.append(processes[i])  
                new_processes_num+=1
            else: break
        toArrive += new_processes_num

        #compare running time of arrived porccesses with remaning time and context swithcing time for current
        for i in range(len(arrived)):
            if(currently_running>=len(arrived) or arrived[i].idd!=arrived[currently_running].idd
             and arrived[i].burst_time<arrived[currently_running].burst_time + context_switching_time):
                currently_running=i

        # time before running any process
        if(last_proccess_id!=arrived[currently_running].idd):
            time += context_switching_time
        
        #run
        curr_porccess_finsihed = quantum >= arrived[currently_running].burst_time
        #save start time and end time 
        startTime=time
        #save processid  note: even if process removed new process will come has different id so there is overhead  @ beggining (TA)
        last_proccess_id = arrived[currently_running].idd 
        if(curr_porccess_finsihed):
            time += arrived[currently_running].burst_time
            finish_time[arrived[currently_running].idd]=time            
            arrived.pop(currently_running)
            finish+=1
        else: 
            time+=quantum
            arrived[currently_running].burst_time-=quantum
        endTime=time
        #save running time into dictinary
        runing_times[(startTime,endTime)]= last_proccess_id
        
    #Waiting,Turnaround,WeightedTurnaround
    metric = np.zeros((len(processes),3)).astype(np.float)

    #filling 
    for i in range(len(processes)):
        metric[i,1] = finish_time[processes[i].idd]-processes[i].arrival_time # TAT = finish - arrival
        metric[i,0] = metric[i,1] = processes[i].burst_time # Wating = TAT - burst_time
        metric[i,2] = 1.*metric[i,1] / processes[i].burst_time # WTAT = TAT/burst_time
   
    return metric,runing_times
    