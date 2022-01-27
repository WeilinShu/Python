#Weilin Shu
#Scores class to read in data and print selected data
import copy

def PrintName(method):             #How to write a decorator
    def wrapper(*args, **kwargs):
        print(" ")
        print(method.__name__)                 #Print method name 
        result = method(*args, **kwargs)       #main return line of decorator
        return result
    return wrapper

class scores :
    #Constructor of the class
    def __init__(self, filename):
        self.filename = filename
        self.readfile()
        
    #This method read the first line of the table in txt and found out the number of the columns. 
    #Then it build up multiple list depend on amount of the columns
    def readfile(self):
        try: 
            Countrylist = [] 
            with open(self.filename) as infile :
                fileContents = infile.readline()
                Countrylist = fileContents.split()        #Generate a Country list save the elements from the first line       
                infile.seek(0)                            #Make the iterator to back to the first line
                self.table = []
                List1 = []
                for columnindex in range (len(Countrylist)):     #Go thought the text file x times. (x=the number of countries)
                    for line in infile:   
                        List1.append(line.split()[columnindex])  #Save each column into a nest list called table
                    infile.seek(0)    
                    self.table.append(List1)
                    List1 = []     
                #This two line build a generator that is required for method 4
                self.sorteddicforMethod4 = sorted(self.table,key= lambda x:x[0])  
                self.GenforMethod4 = (elem for elem in self.sorteddicforMethod4)                     
        except:
            print("Error opening " + self.filename)
            raise SystemExit

    #This method prints all country abbreviations and their corresponding scores,
    #sorted by the total score of each country
    @PrintName
    def printbytotal(self):
        totaltable = self.table
        totaldic = {}
        totaldic = {e[0] : e[1:] for e in totaltable}
        sorteddic = sorted(totaldic.items(),key= lambda x:sum(list(map(int,x[1]))))
        for k,v in sorteddic:
            print("{:<4s}". format(k + ":"), end = " ")
            for i in v:
                print ("{:>4s}". format(i), end = " ")            
            print ("\n", end = "")
        print (" ")


    #This method accepts a score limit and a boolean for going above or below the limit
    @PrintName
    def findLimit(self, limit, GreaterOrSmaller):          
        table = self.table
        dic = {}
        dic = {e[0] : e[1:] for e in table}  
        if GreaterOrSmaller == "a":
            list1= []
            valueGen = (elem for elem in dic.values())
            keyGen = (elem for elem in dic.keys())
            for i in range (len(table)):
                if any (elem > limit for elem in list(map(int,next(valueGen)))):
                    list1.append(next(keyGen))        
                else:
                    next(keyGen)
            print ("Countries with scores above " + str(limit) + " :", end = ' ')
            for i in list1:
                print (i, end = ' ')
            print ("\n", end = "")
            print (" ")
        elif GreaterOrSmaller == "b":
            list2= []
            valueGen = (elem for elem in dic.values())
            keyGen = (elem for elem in dic.keys())
            for i in range (len(table)):
                if any (elem < limit for elem in list(map(int,next(valueGen)))):
                    list2.append(next(keyGen))        
                else:
                    next(keyGen)
            print ("Countries with scores below " + str(limit) + " :", end = ' ')
            for i in list2:
                print (i, end = ' ')       
            print ("\n", end = "")
            print (" ")
                
                
    #A method that prints the frequency of all the scores. Each unique score is printed with
    #its frequency count on one line.
    @PrintName
    def PrintFrequency (self):
        table1 = copy.deepcopy(self.table) 
        for ind in table1:
            ind.pop(0)
        mylist = []
        for x in table1:
            for y in x:
                mylist.append(y)
        myDic = {i:mylist.count(i) for i in mylist}
        sorteddic = sorted(myDic.items(),key=lambda x:int(x[0]))
        for k, v in sorteddic:
            print (k +(":")+ str(v))
        print (" ")
        
        
        
    #A method which is a generator that returns one country's record at a time. 
    def PrintOneByOne(self):
        try:
            print (" ".join(next(self.GenforMethod4)))
            return False
        
        except StopIteration:
            print("All country records are printed")
            print(" ")
            return True
            
        
