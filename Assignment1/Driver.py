#Weilin Shu
#Driver code that uses Scores class
import Scores

#This method print Menu    
def printingMenu():   
    print ("1. Print by total score")
    print ("2. Print by limit")
    print ("3. Print one")
    print ("4. Print score frequency")
    print ("5. Quit")
  
# Function that call ReadFile from Scores
def callReadFile(s):
    Scores.scores.readfile(s)

# Function that calls the Scores object method 1 to print all records sorted by the total scores.       
def callprintbytotal (s):
    Scores.scores.printbytotal(s)

#  Function that prompts the user for a score limit and a choice of above or below the limit. 
#  Then the function calls the Scores object method 2. If the user enters an invalid limit or invalid choice, re-prompt until there is valid input.
def callfindLimit (s):
    #This while loop checks if the user enter numbers       
    validInput1 = False
    while not validInput1:
        try:
            limit = int(input("What is the limit? "))
            validInput1 = True
        except ValueError:
            print ("Limit must be a number")
    #This while loop checks if the user enter the correct above/below option
    validInput2 = False
    while not validInput2:
        GreaterOrSmaller = input("Above or Below " + str(limit) + ("? (a/b) "))
        if GreaterOrSmaller == "a" or GreaterOrSmaller == "b":
            validInput2 = True
        else:
            print ("Must be 'a' or 'b'!")
            validInput2 = False                    
    Scores.scores.findLimit(s, limit, GreaterOrSmaller)

# Function that calls the Scores object method 3 to print the frequency of the scores.
def callPrintFrequency (s):
    Scores.scores.PrintFrequency(s)

    

#A function that will make loop to let the user press the Enter key to see one country record at a time. 
#The loop ends when the user enters any other character, or when there is no more country record.
def callPrintOneByOne (s):
    ifFinish = False
    while not ifFinish:
        userinput = input("Press enter key to print a country record, or enter any character to end:")
        if not userinput:    
            ifFinish = Scores.scores.PrintOneByOne(s)
        else:
            print (" ")
            break

# Main fuction that create a Scores object
# Loop to call the function of item 1 above until the user chooses 5.

def getInput():
    printingMenu() 
    UserInput = int(input("Enter a choice: "))  
    return UserInput


def main():
    scoreTable = Scores.scores("input1.txt")
    optionlist = [0, callprintbytotal, callfindLimit, callPrintOneByOne,callPrintFrequency]
    printingMenu() 
    UserInput = int(input("Enter a choice: "))
    while UserInput !=5:
        try:
            if UserInput >=1 and UserInput <=4 :     
                optionlist[UserInput](scoreTable) 
                UserInput = getInput()
            else:
                print ("Please put in 1-5"+"\n")
                UserInput= getInput()
        except ValueError:
            print ("Please input number only" + "\n")
            UserInput =getInput()

    
main()