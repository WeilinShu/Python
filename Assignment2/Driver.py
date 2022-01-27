#Weilin Shu
#Driver code that uses Scores class
import Enrolldata

def printingMenu():   
    print ("1. Calculate and plot the enrollment trend")
    print ("2. Calculate and plot the age groups")
    print ("3. Quit")
    
def callReadFile(s):
    Enrolldata.enrolldata.readfile(s)
    
def callanalysistrend (s):
    Enrolldata.enrolldata.analysistrend(s)
    
def callanalysistagegroup(s):
    select = int(input("Enter a choice:1,2014 2,2015 3,2016 4,2017: "))
    Enrolldata.enrolldata.analysistagegroup(s,select)
    
def main():
    DataTable = Enrolldata.enrolldata("students1.csv")
    while True:
        try:
            printingMenu()
            UserInput = int(input("Enter a choice: "))
            if UserInput >=1 and UserInput <=2 :    
                optionlist = [0, callanalysistrend, callanalysistagegroup]
                optionlist[UserInput](DataTable)
            elif UserInput == 3:
                break            
            else:
                print ("Please put in 1-3"+"\n")                  
        except ValueError:
            print ("Please input number only" + "\n")        
                
main()