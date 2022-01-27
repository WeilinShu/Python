#Weilin Shu
#Lab2 class have GUI code to create 3 window classes

import Enrolldata
import matplotlib
matplotlib.use('TkAgg')               	# tell matplotlib to work with Tkinter
import tkinter as tk                      	# normal import of tkinter for GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt
import  tkinter.messagebox  as  tkmb


filename = "students2.csv"

def notabletoclose():
    print("not able to close")

def nowIcanclose(me):
    me.destory()

class Mainwindow() :
    def __init__(self,master):
        '''
        The constructor
        '''

        self.master= master
        self.master.geometry("300x200")
        self.master.title("Lab2")
        self.ifprint = False
        L = tk.Label(self.master, text = "Enrollment data for California Community Colleges" , fg ="blue")
        L.pack(side="top")
        B1 = tk.Button(self.master, text="Enrollment Trend", command=self.callanalysistrend)
        B1.pack()
        B2 = tk.Button(self.master, text="Enrollment Age", command=self.callDialogwindow )
        B2.pack()  
        self.diawin = None 
    
        self.DataTable = Enrolldata.enrolldata(filename)
        
    def callanalysistrend(self):
        '''
        This method calls analysistrend from Enrolldata file
        '''
        newwin2 = tk.Toplevel()
        plotwindow = Plotwindow(newwin2, lambda: self.DataTable.analysistrend(newwin2))
        
    def callDialogwindow(self):
        '''
        This method opens a dialogwindow object
        '''
        self.diawin = tk.Toplevel()
        dialogwindow = Dialogwindow(self.diawin,self.DataTable,self.master)
        self.master.wait_window(dialogwindow)
        
        
        
class Dialogwindow(tk.Toplevel) :
    def __init__(self,master,DataTable,root):
        '''
        The constructor
        '''        
        self.root = root
        self.DataTable = DataTable
        self.master= master
        self.master.geometry("300x350")
        self.master.title("Enrollment by Age")        
        controlVar = tk.IntVar() 
        self.plotwin = None
        master.grab_set()
        master.focus_set()
        #self.root.protocol('WM_DELETE_WINDOW', notabletoclose) 

        
        c=[]
        for i in range(len(self.DataTable.yeararray)):
            c.append(tk.Radiobutton(master, text=self.DataTable.yeararray[i], variable=controlVar, value=i+1))
            c[i].grid()
            i=i+1
       
        B = tk.Button(master, text="OK", command=lambda: self.callanalysistagegroup(controlVar.get()-1))   
        B.grid()
        


        
    def callanalysistagegroup(self,select):
        '''
        This method calls analysistagegroup from Enrolldata file
        '''
        #self.root.protocol('WM_DELETE_WINDOW', nowIcanclose(self.root)) 
        if (self.plotwin is not None) and self.plotwin.winfo_exists():
            state = tkmb.askokcancel("Confirmation","Plot already open, Do you want to open another one?", parent=self.master)
            if state == True :     # when the user clicks OK
                self.plotwin = tk.Toplevel()      
                plotwindow = Plotwindow(self.plotwin,lambda:self.DataTable.analysistagegroup(select,self.plotwin))
        else:    
            self.plotwin = tk.Toplevel()      
            plotwindow = Plotwindow(self.plotwin,lambda:self.DataTable.analysistagegroup(select,self.plotwin))   

            
        
        
        
class Plotwindow(tk.Toplevel):
    '''
    The constructor
    '''    
    def __init__(self,master,method):
        self.master= master
        self.root = root
        master.geometry("700x700")
        master.title("CCC Enrollment") 
        fig = plt.figure(figsize=(40, 40))   
        method()    
        canvas = FigureCanvasTkAgg(fig, master=master)      # create canvas with figure that matplotlib used
        canvas.get_tk_widget().pack()                        # position canvas
        canvas.draw()            
        self.master.focus_set()
        
        
        
def closeeverything():
    root.destroy()  


root = tk.Tk()    #please remove root
main = Mainwindow(root)
root.protocol('WM_DELETE_WINDOW', closeeverything) 
root.mainloop()

    
    
    
'''
Accounding to the search of CA economy in 2009, there is a global financial crisis hitting the California economy
Compare it to the graph, there is a large decreasing numbers from 2009 to 2018. I believe that this descreasing is due to the finacial crisis.
But there are actually more young adult between age 20-24 in school now, I think it is because of bad economy, it's better just study than waste time making less money...
'''