#Weilin Shu
#Lab3front make GUI application. Use the database that's built by lab3back.py for input.

from lab3back import Lab3back
import tkinter as tk
import numpy as np

class Mainwindow(tk.Tk) :
    def __init__(self):
        '''
        The constructor
        '''
        super().__init__()                        #Must have 
        self._getFile()                           
        self.title("Movie Guide")
        self.geometry("550x300")
        F = tk.Frame(self)                        #Create  a frame 
        B1 = tk.Button(F, text="Genre" ,command = self.printbygenre)
        B2 = tk.Button(F, text="Rating", command =self.printbyrate )
        B1.grid(row = 0, column =0)
        B2.grid(row = 0, column =2) 
        F.grid(sticky = 'n')       
        F2 = tk.Frame(self) 
        self.Sc = tk.Scrollbar(F2)
        self.Sc.grid(sticky='ns', row=1,column =1)          #Make sticky ns !!!
        self.LB = tk.Listbox(F2, height=7, width=80, yscrollcommand=self.Sc.set)  #yscrollcommand associate listbox with scrollbar
        self.Sc.config(command=self.LB.yview)
        self.LB.grid(row=1,column =0)
        F2.grid(sticky = 'n')
        self.Data = ''
        self.L = tk.Label(self, text=self.Data)  
        self.L.grid(sticky = 'w')


    def _getFile(self) :
        '''
        This function makes a Lab3back object
        '''
        self._d = Lab3back()
        
    def printbygenre(self):
        '''
        This function calls GetGenreList and GetMoviesByGenre from Lab3Back, makes the dialogwindow and get user selection for specific genre
        '''
        self.L['text'] = ''
        self.LB.delete(0, tk.END)  
        genreWin = DialongWin(self,self._d.GetGenreList(),'genre',len(self._d.GetGenreList()))
        self.wait_window(genreWin)
        self.L['text'] = str(self._d.GetGenreList()[genreWin.getChoice()])
        self.Data = self._d.GetMoviesByGenre(genreWin.getChoice()+1)
        Text = [item[1] for item in self._d.GetMoviesByGenre(genreWin.getChoice()+1)]
        self.LB.insert(tk.END,  *Text)
        self.LB.bind("<ButtonRelease-1>",self.Getmovieinfo)
            
        
    def printbyrate(self):
        '''
        This function calls GetMoviesByRate from Lab3Back, makes the dialogwindow and get user selection for specific rate
        '''
        self.L['text'] = ''
        self.LB.delete(0, tk.END)  
        list = np.arange(0,5.1,0.5)[::-1]
        rateWin = DialongWin(self, list, 'rate', len(list),' star','s')
        self.wait_window(rateWin)
        if(5 - 0.5 * rateWin.getChoice() <=5 ):
            self.L['text'] = str(5 - 0.5 * rateWin.getChoice())+' stars'
            self.Data = self._d.GetMoviesByRate(5 - 0.5 * rateWin.getChoice())
            Text = [item[1] for item in self._d.GetMoviesByRate(5 - 0.5 * rateWin.getChoice())]    
            self.LB.insert(tk.END,  *Text)
            self.LB.bind("<ButtonRelease-1>",self.Getmovieinfo)            
            
    def Getmovieinfo(self,event):
        '''
        This fuction print the complete movie info
        '''
        self.L['text'] = str(self.Data[self.LB.curselection()[0]][2])+' stars ' + 'released: '+str(self.Data[self.LB.curselection()[0]][4])+' genre: '+str(self.Data[self.LB.curselection()[0]][6])    
        
        
class DialongWin(tk.Toplevel):
    def __init__(self,master,thelist, typename, nrange,*args, **kargs):
        '''
        DialongWindow constructor
        '''
        super().__init__(master)
        self.title("Choose a "+typename)
        self.geometry("250x350")
        self.controlVar = tk.IntVar() 
        self.controlVar.set(0)
        #print(args)
        
        
        if typename == 'rate' :
            for i in range(nrange):
                if i > 7:
                    tk.Radiobutton(self, text=str(thelist[i])+str(args[0]), variable= self.controlVar,value = i).grid(sticky = "w")
                elif i <= 7:
                    tk.Radiobutton(self, text=str(thelist[i])+str(args[0])+str(args[1]), variable= self.controlVar,value = i).grid(sticky = "w")
                    
        elif typename == 'genre':
            for i in range(nrange):
                tk.Radiobutton(self, text=str(thelist[i]), variable= self.controlVar,value = i).grid(sticky = "w")

        B = tk.Button(self, text="OK",command=self.destroy)
        B.grid()
        self.grab_set()
        self.focus_set()        
        self.protocol("WM_DELETE_WINDOW", self._close)     
        self.transient(master)
    
    def getChoice(self) :  
        '''
        This fuction return the userchoice
        '''
        return(self.controlVar.get())

    def _close(self) :
        '''
        This function reset controlvar when user close the window
        '''
        self.controlVar.set(-1)
        self.destroy()    
        
    
win = Mainwindow()
win.mainloop()