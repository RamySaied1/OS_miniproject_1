from RR import RR
#import HPF
from tkinter import *


def Gui():
    window = Tk()
    window.title("Scheduling simulation")
    window.geometry('600x400')
    lbl_RR = Label(window,text='Round Robin')
    lbl_RR.grid(column=1, row=1)
    rad1 = Radiobutton(window,text=' First', value=1)
    rad2 = Radiobutton(window,text=' Second', value=2)
    rad3 = Radiobutton(window,text=' Third', value=3)
    rad1.grid(column=1, row=2)
    rad2.grid(column=1, row=3)
    rad3.grid(column=1, row=4)
    btn = Button(window, text="simulate", command=simulate)
    btn.grid(column=1, row=5)
    window.mainloop()


def readProcess():
    f=open("output.txt",'r')
    lines=f.readlines()
    processes = [list(map(float,i.split())) for i in lines[1:int(lines[0])]]
    f.close()
    return processes
    

def simulate():
    processes=readProcess()
    #TODO read choice form gui
    choice =0
    if(choice == 0):
        RR(processes)

processes=[]
def main():
    #Gui()
    simulate()


if __name__ == '__main__':
    main()







