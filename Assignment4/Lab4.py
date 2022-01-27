#Weilin Shu

LOCAL_ZIP = [92093, 90013, 95192, 94132, 94720, 95064, 95819, 92697, 93940, 94544]

import tkinter as tk
import json
import requests
import tkinter.messagebox  as  tkmb
import tkinter.filedialog
import os
import time
import threading


class Mainwindow(tk.Tk) :
    def __init__(self):
        super().__init__()
        self.title("Welcome to the weather app")
        self.geometry("550x300")
        F1 = tk.Frame(self)   
        B1 = tk.Button(F1, text="Choose a City",command = self.printdata).grid(row = 0, column =0)
        self.Sc = tk.Scrollbar(F1)
        self.Sc.grid(sticky='ns', row=1,column =1)
        self.LB = tk.Listbox(F1, height=10, width=80, yscrollcommand=self.Sc.set)
        self.Sc.config(command=self.LB.yview)
        self.LB.grid(row=1,column =0)
        F1.grid(sticky = 'n',row = 0, column =0)
        self.grid_rowconfigure([0,1], weight=1)   
        self.grid_columnconfigure(0, weight=1)
        
        d = threading.Thread(target=self.getInfo, args=())
        d.setDaemon(True)
        d.start()
        self.save = []
        self.protocol("WM_DELETE_WINDOW", self._ASKSAVE)     

    def getInfo(self):
        self.result = []
        start = time.time() 
        threads = []  
        for i in LOCAL_ZIP:
            t = threading.Thread(target = self.fetchdata, args = (i,))
            threads.append(t)
            t.start()
        for t in threads :
            t.join()            
            
        print("Total elapsed time: {:.2f}s".format(time.time()-start))
        #with open('weather.json', 'w') as fh:
        #    json.dump(result, fh,indent=3)            
        #with open('weather.json', 'r') as fh: 
        #    data = json.load(fh)
        self.info = []
        for i in self.result:
            self.info.append([i['name'],i['main']['temp'],i['weather'][0]['description']])
        self.info = sorted(self.info,key= lambda x:x[0])  
        
             
        
    
    def fetchdata(self, zip):
        page = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+str(zip)+',us&units=imperial&APPID=878b0d58df1ed656428e4e31a4f821db')
        print(page.json())
        self.result.append(page.json())
        
    def printdata(self):
        cityWin =  DialongWin (self, self.info)
        self.wait_window(cityWin)
        Text = self.info[cityWin.getChoice()][0]+': '+str(round(self.info[cityWin.getChoice()][1]))+' degrees, '+self.info[cityWin.getChoice()][2]
        self.save.append(Text)
        self.LB.insert(tk.END,  Text)
        
    def _ASKSAVE(self):
        if len(self.save) != 0:
            state = tkmb.askokcancel("Save","Save your search in a directory of your choice?", parent = self)
            if state == True:
                directory  = tk.filedialog.askdirectory(initialdir= ".")
                if not directory:
                    tkmb.showinfo('Save', 'No save being made', parent=self)          
                    self.destroy()
                    raise SystemExit()
                if os.path.isfile( directory+'/weather.txt' ):
                    os.remove( directory+'/weather.txt' )
                self.writeFile(os.path.join(directory,'weather.txt'), self.save)         
                tkmb.showinfo('Save', 'File weather.txt will be saved in \n'+ directory, parent=self)            
                self.destroy()
            elif state == False:
                self.destroy()
        else:
            self.destroy()
    
    def writeFile(self,filename, list):
        print(list)
        fh = open(filename, 'a')
        for i in list:
            fh.write(i)
            fh.write('\n')
        fh.close()
    
class DialongWin(tk.Toplevel):
    def __init__(self,master, info):
        super().__init__(master)
        self.title("Choose a city")
        self.geometry("250x350")
        self.controlVar = tk.IntVar() 
        self.controlVar.set(0)
        
        for i in info:
            tk.Radiobutton(self, text=i[0], variable= self.controlVar,value = info.index()).grid(sticky = "w")
            
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