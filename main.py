#import HPF
from Process import Process
from RR import RR
from SNRT import SNRT
from HPF import HPF
from FCFS import FCFS
from process_generator import generate_process
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

class Gui:
    def __init__(self):
        self.window=tk.Tk()
        self.window.title("Scheduling simulation")
        self.window.minsize(width=750, height=600)
        self.window.maxsize(width=750, height=600)
        self.algo = tk.IntVar(self.window,-1)
        self.generate_input_file_name_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, "./input.txt"))
        self.generate_output_file_name_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, "./output.txt"))
        self.processes_file_name_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, "./processes.txt"))
        self.statistics_file_name_entry = tk.Entry(self.window, textvariable=tk.StringVar(self.window, "./statistics.txt"))
        vcmd=(self.window.register(lambda s,S :s.isdigit() or s=='' or s=='.' and S.count('.')<= 1),'%S','%P')
        self.context_switching_time_entry=tk.Entry(self.window,textvariable=tk.StringVar(self.window,'0'),validate='key',vcmd=vcmd)
        self.quantum_entry=tk.Entry(self.window,textvariable=tk.StringVar(self.window,'2'),validate='key',vcmd=vcmd)
        
        row=0
        tk.Label(self.window,text='generate input file:',justify = tk.LEFT).grid(row=row,column=0,sticky='W',padx=10);row+=1
        self.generate_input_file_name_entry.grid(row=row,column=0,sticky='W',padx=10);row+=5
        tk.Label(self.window,text='generate output file:',justify = tk.LEFT).grid(row=row,column=0,sticky='W',padx=10);row+=1
        self.generate_output_file_name_entry.grid(row=row,column=0,sticky='W',padx=10);row+=5        
        tk.Button(self.window,text="Generate",command=self.generate).grid(row=row,column=0,padx=10,pady=1,sticky='W');row+=10
        tk.Label(self.window,text='processes file:',justify = tk.LEFT).grid(row=row,column=0,sticky='W',padx=10);row+=1
        self.processes_file_name_entry.grid(row=row,column=0,sticky='W',padx=10);row+=5
        tk.Label(self.window, text='statistics file:', justify=tk.LEFT).grid(row=row, column=0, sticky='W', padx=10);row += 1
        self.statistics_file_name_entry.grid(row=row, column=0, sticky='W', padx=10);row += 5
        tk.Label(self.window,text='context switching time:',justify = tk.LEFT).grid(row=row,column=0,sticky='W',padx=10);row+=1
        self.context_switching_time_entry.grid(row=row,column=0,sticky='W',padx=10);row+=5
        tk.Label(self.window,text='quantum:',justify = tk.LEFT).grid(row=row,column=0,sticky='W',padx=10);row+=1
        self.quantum_entry.grid(row=row,column=0,sticky='W',padx=10);row+=5
        
        row+=10
        algos=[("HPF",0),("FCFS",1),("RR",2),("SRTN",3)]
        tk.Label(self.window,text='Choose Algorithm:',justify = tk.LEFT).grid(row=row,column=0,sticky='W',padx=10);row+=1
        for text, algo in algos:
            tk.Radiobutton(self.window,text=text,variable=self.algo,value=algo).grid(row=row,column=0,padx=10,pady=1,sticky='W');row+=1
        
        tk.Button(self.window,text="Simulate",command=self.simulate).grid(row=row,column=0,padx=10,pady=1,sticky='W')
        
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(self.figure, master=self.window)
        canvas.get_tk_widget().grid(row=0, column=50, rowspan=100,pady=5,stick='E')



    def statistics(self, metric, output_file):  # to save statistics of running algorithm in specific file
        output = open(output_file, 'w')
        output.writelines('process_id'.ljust(15) + 'waiting time'.ljust(15) + 'TAT'.ljust(15)+'WTAT'.ljust(15)+'\n')
        sum_tat=0;
        sum_wtat=0;
        for i in range(0, len(metric)):
            sum_tat = sum_tat+metric[i, 2]
            sum_wtat= sum_wtat+metric[i,3]
            output.writelines(str(int(metric[i, 0])).ljust(15)+ str(round(metric[i, 1],3)).ljust(15)
            + str(round(metric[i, 2],3)).ljust(15) + str(round(metric[i,3],3)) +'\n')
        
        output .writelines('\nAVG TAT = '+str(round(sum_tat/len(metric),3)) +'\n')
        output .writelines('AVG WTAT = '+str(round(sum_wtat/len(metric),3))+'\n')


    def barChart(self,running_times):
        # al x values , y values and widthes
        xs = []
        ys = []
        ws = []
        for k,v in running_times.items():
            xs.append(k[0])
            ys.append(v)
            ws.append(k[1]-k[0])

        self.subplot.cla()
        self.subplot.bar(xs,ys,ws,align='edge')
        canvas = FigureCanvasTkAgg(self.figure, master=self.window)
        canvas.get_tk_widget().grid(row=0, column=50,columnspan=100, rowspan=100,pady=5,stick='E')
        toolbarframe = tk.Frame(self.window)
        toolbarframe.grid(row=102, column=50,sticky='W')
        toolbar = NavigationToolbar2Tk(canvas, toolbarframe)
        toolbar.update()

    def simulate(self):
        try:
            fileName = self.processes_file_name_entry.get()
            statistics_file_name = self.statistics_file_name_entry.get()
            context_switching_time = float(self.context_switching_time_entry.get())
            quantum = float(self.quantum_entry.get())
            algo = self.algo.get()
            processes = self.readProcess(fileName)
            assert len(processes)>0 ,"Wrong File Name or Empty file. No Processes Read !!!"
            assert algo != -1 ,"Please Choose an algorithm !!!"

            metric,running_times=(None,None)
            if(algo == 0):
                metric, running_times = HPF(processes, context_switching_time)
            elif(algo == 1):
                metric, running_times = FCFS(processes, context_switching_time)
            elif(algo == 2):
                assert quantum!=0,"Please Enter valid quantum !!!"
                metric,running_times = RR(processes,context_switching_time,quantum) 
            elif(algo == 3):
                metric,running_times = SNRT(processes,context_switching_time)

            self.statistics(metric, statistics_file_name)
            self.barChart(running_times)
        except Exception as err:
            tk.messagebox.showerror("Error",str(err))

    def generate(self):
        try:
            in_file = self.generate_input_file_name_entry.get()
            out_file = self.generate_output_file_name_entry.get()
            print(in_file,out_file)
            generate_process(in_file,out_file)
            tk.messagebox.showinfo("","Proccesses Generated")
        except Exception as err:
            tk.messagebox.showerror("Error",str(err))


    def readProcess(self,filename):
        f=open(filename,'r')
        lines=f.readlines()
        processes = []
        for i in lines[1:int(lines[0])+1]:
            p = ( list( map(float,i.split()) ) )
            processes.append(Process(int(p[0]),p[1],p[2],p[3]))
            
        f.close()
        return processes
    
    


processes=[]
def main():
    Gui().window.mainloop()


if __name__ == '__main__':
    main()







