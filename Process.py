class Process:
    def __init__(self, idd,arrival_time, burst_time,priority,start_time=0,finish_time=0):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.finish_time = finish_time
        self.start_time = start_time
        self.idd = idd



