#Weilin Shu
#Enrolldata class read data from given file, plot the enrollment trend 
#and plot the number of students in each age group
import csv
import numpy as np
import matplotlib
matplotlib.use('TkAgg') 
import tkinter as tk  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
import matplotlib.pyplot as plt
import numpy as np
import  tkinter.messagebox  as  tkmb


def showNums(method):
    '''
    This is the decorator applied to the methods of steps 3 and 4, 
    will print to the output screen the array that's returned. 
    '''
    def wrapper(*args, **kwargs):
        result = method(*args, **kwargs)
        print(*result)
        return result
    return wrapper

class enrolldata :    
    def __init__(self, filename):
        '''
        The constructor
        '''
        self.filename = filename
        self.readfile()
        
    def readfile(self):
        '''
        Readfile method read in the file, create two np array 
        the yeararray store the years, and a 2d np array to hold data
        '''
        try:
            self.yeararray = []
            self.table = np.array([]) 
            with open(self.filename) as infile:
                reader1 = infile.readline()
                self.yeararray = np.asarray(list(map(int,reader1.split(","))))
                reader2 = csv.reader(infile)                               
                self.table = np.loadtxt(self.filename,dtype = int,delimiter = "," ,skiprows =1)
                #self.table = np.array(list(reader2), dtype = int)     #Same effect 
        except FileNotFoundError:
            root = tk.Tk()
            tkmb.showerror('Error', 'Cannot open File ' + self.filename + '\nCheck the file and try again', parent=root)
            raise SystemExit        
    
    @showNums        
    def analysistrend (self,master):
        '''
        analysistrend method calculate and plot the enrollment trend using data
        '''
        
        sumYear = self.table.sum(0)
        plt.plot(self.yeararray,sumYear/1000000)
        plt.title("Number of Students VS The Years")     
        plt.xlabel("Year")
        plt.ylabel("Number of students(Millions)")
        #print(len(self.yeararray))
        plt.xticks(np.arange(self.yeararray[0],self.yeararray[len(self.yeararray)-1]+1), self.yeararray) 
        
        return sumYear
    
    @showNums    
    def analysistagegroup (self,select,master):   
        '''
        analysistagegroup method calculate and plot the age groups:
        '''
        #print(self.table[:,0])
        print(select)  
        preadd = self.table[:,select-1];
        sumarray =[]
        sum = 0
        #preadd.sum(axis =0)
        #print(*preadd)        
        for i in range (0,8):
            for j in range(0,6):
                sum = sum + preadd[j*8+i]    
            sumarray.append(sum)
            sa = np.asarray(sumarray)
            sum = 0
        print(*sumarray)
        plt.bar((1,2,3,4,5,6,7),sa[0:7]/1000)
        #plt.plot(np.arange(1,8),sa[0:7]/1000000)
        plt.title("Number of Students Per Age Group in " + str(self.yeararray[select])+" (Thousands)") 
        label = ["19orless","20-24","25-29","30-34","35-39","40-49","50+"]        
        plt.xlabel("Age")
        plt.ylabel("Number of students(Thousands)")
        plt.xticks((1,2,3,4,5,6,7), label)
       

        return sa
        
