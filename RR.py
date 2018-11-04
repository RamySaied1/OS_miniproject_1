from Process import Process

def RR(processes,quant=1):
    queue = list([])
    processes.sort(key=lambda elem: (elem[1],elem[0]))
    time =0
    turn=0
    for i in processes:
        if(time == i[1]):
            queue.append()
    #process number, arrival time, burst time and priority. 
    #while(len(processes))