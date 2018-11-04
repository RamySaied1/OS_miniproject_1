import numpy as np
import os


def generate_process(input_file,output_file):

    input  = open(input_file, 'r') 

    lines=input.readlines()

    ## read and check on input file parameters
    if len(lines)<4 :
        print(" file size > 4 lines")
        return

    try:
        num_process=int(lines[0])
    except ValueError:
        print("error in number of process parameter")
        return
    try:
        priority = int(lines[3])
    except ValueError:
        print("error in prioity parameter")
        return

    arrival=(lines[1]).split()
    if len(arrival)!=2:
        print(" error in  arrival time parameters")
    
    for i in range(0,2):
        try:
            arrival[i]=float(arrival[i])
        except ValueError:
            print("error in getting arrival time parameters")
            return

    burst = (lines[2]).split()
    if len(burst) != 2:
        print(" error in burst time parameters")

    for i in range(0,2):
        try:
            burst[i] = float(burst[i])
        except ValueError:
            print("error in  burst time parameters")
            return

    input.close()

    ### generate process and write them to the output file
    output = open(output_file, 'w')
    output.writelines(str(num_process)+'\n')

    for i in range(0,num_process):
        
        arrival_time=round(np.random.normal(arrival[0],arrival[1]),1)
        while arrival_time<0:
            arrival_time = round(np.random.normal(arrival[0], arrival[1]), 1)

        burst_time = round(np.random.normal(burst[0], burst[1]),1)
        while burst_time <= 0:
            burst_time = round(np.random.normal(burst[0], burst[1]), 1)

        prioty_value = np.random.poisson(priority)
        output.writelines(str(i+1) + " "+str(arrival_time) +
                          " "+str(burst_time)+" "+str(prioty_value)+'\n')

                          
    output.close()

    
generate_process("os_project/input.txt", "os_project/output.txt")

