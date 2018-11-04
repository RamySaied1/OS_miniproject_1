class Process:
    def __init__(self, idd,arrival_time, burst_time,priority,start_time,finish_time):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.finish_time = finish_time
        self.start_time = start_time
        self.idd = idd



def RR():
    queue = list()
    in_file = open('output.txt','r')
    processes = [list(map(float,i.split())) for i in in_file.readlines()[1:]]
    #process number, arrival time, burst time and priority
    


RR()

