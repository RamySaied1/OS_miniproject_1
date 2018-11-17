#import HPF
from Process import Process
from RR import RR
from SNRT import SNRT
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
        self.file_name_entry=tk.Entry(self.window,textvariable=tk.StringVar(self.window,"processes.txt"))
        vcmd=(self.window.register(lambda s,S :s.isdigit() or s=='' or s=='.' and S.count('.')<= 1),'%S','%P')
        self.context_switching_time_entry=tk.Entry(self.window,textvariable=tk.StringVar(self.window,'0'),validate='key',vcmd=vcmd)
        self.quantum_entry=tk.Entry(self.window,textvariable=tk.StringVar(self.window,'2'),validate='key',vcmd=vcmd)
        
        row=0
        tk.Label(self.window,text='file name:',justify = tk.LEFT).grid(row=row,column=0,sticky='W',padx=10);row+=1
        self.file_name_entry.grid(row=row,column=0,sticky='W',padx=10);row+=5
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


    def barChart(self,running_times):
        # al x values , y values and widthes
        xs = []
        ys = []
        ws = []
        for k,v in running_times.items():
            xs.append(k[0])
            ys.append(v+1)
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
            fileName = self.file_name_entry.get()
            context_switching_time = float(self.context_switching_time_entry.get())
            quantum = float(self.quantum_entry.get())
            algo = self.algo.get()
            processes = self.readProcess(fileName)
            assert len(processes)>0 ,"Wrong File Name or Empty file. No Processes Read !!!"
            assert algo != -1 ,"Please Choose an algorithm !!!"

            metric,running_times=(None,None)
            if(algo == 0):
                0
            elif(algo == 1):
                1
            elif(algo == 2):
                assert quantum!=0,"Please Enter valid quantum !!!"
                metric,running_times = RR(processes,context_switching_time,quantum)  
            elif(algo == 3):
                metric,running_times = SNRT(processes,context_switching_time)

            self.barChart(running_times)
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
    #simulate()


if __name__ == '__main__':
    main()







