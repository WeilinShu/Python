import socket
import time
import multiprocessing as mp
import platform
import pickle

def highlevelchild(qsent, qget):
    while True:
        list1 = qsent.get()
        if list1 == 0:
            break
        list1.append(list1[-1]+1)
        qget.put(list1)
    

def highlevel():
    '''
    A highLevel function that: 
    a.Creates a child process that uses a multiprocessing object to pass data to the main process.
    b.The main process and child process will pass data back and forth in a loop, with a timer that starts right before the loop begins and ends right after the loop ends. 
    c.The function returns the ratio:  number of one-way data transfer / time difference.
    '''

    qsent = mp.Queue()
    qget = mp.Queue()
    e = mp.Event()
    p = mp.Process(target = highlevelchild, args = (qsent,qget))           # 1,create a child process and the data transfer mechanism
    p.start()
   

    list1 = [1]
    qsent.put(list1)
    try: 
        list1 = qget.get()
        if list1 != [1,2]:                                                    #2, test that the connection is okay
            raise ValueError("An error occurred")
    except ValueError:
        print("Data not expected, program will end")
        raise SystemExit
    
    list1 = []                                                               # 3,re-initialize the list
    transfernumber = 0
    start = time.time()                                                      # 4,start the timer
    while len(list1) < 300:                                                  # 5,loop 300 times
        list1.append(len(list1)+1)
        qsent.put(list1)
        transfernumber += 1
        #print("sent"+ str(list1)) 
        list1 = qget.get()
        #print("get " + str(list1))
    t = time.time()-start                                                     #6,record the end clock time
    qsent.put(0)                                                              #7,send a 0 to the child so it can terminate
    
    '''
    while not qget.empty():
        num+=1  
        qsent.put(num)
        num = qget.get()        
    '''
    p.join()                                                                  # 8,wait for the child to end
    try: 
        if list1[-1] != 300 and len(list1) != 300:                             #9,verify that the returned data is as expected
            raise ValueError("An error occurred")
    except ValueError:
        print("Data not expected, program will end")
        raise SystemExit
    
    return transfernumber/t                                                    #10, return the ratio


def lowlevelchild():
    '''
    A lowLevel function that: 
    a.=Creates a child process that uses a socket to pass data to the main process.
    b.The main process and child process will pass data back and forth in a loop, with a timer that starts right before the loop begins and ends right after the loop ends. 
    c.The function returns the ratio:  number of one-way data transfers / time difference.
    '''
    HOST = "localhost"      
    PORT = 5554
    with socket.socket() as s :
        s.bind((HOST, PORT))
        s.listen()
        (conn, addr) = s.accept()
        while True:      
            list1 = pickle.loads(conn.recv(4096))
            #print(list1)
            if list1 == 0:
                break                              
            list1.append(len(list1)+1)
            #print(list1)
            conn.send(pickle.dumps(list1))

def lowlevel():    
    HOST = 'localhost'
    PORT = 5554    
    p2 = mp.Process(target=lowlevelchild)                              # 1,create a child process and the data transfer mechanism
    p2.start()     
    
    with socket.socket() as s :
   
        s.connect((HOST, PORT))

        list1 = [1]
        transfernumber = 0
        s.send(pickle.dumps(list1))
        try: 
            list1 = pickle.loads(s.recv(4096))
            if list1 != [1,2]:                                        #2, test that the connection is okay, There's a exception going on here
                raise ValueError("An error occurred")   
        except ValueError:
            print("Data not expected, program will end")
            raise SystemExit            
        
        list1 = []                                                    # 3,re-initialize the list
        start = time.time()                                           # 4,start the timer
        while len(list1) < 300:                                        # 5,loop 300 times
            list1.append(len(list1)+1)
            s.send(pickle.dumps(list1))
            transfernumber += 1
            #print("sent"+ str(list1)) 
            list1 = pickle.loads(s.recv(4096))
            #print("Received from server:"+ str(list1))
            
        t = time.time()-start       #6,record the end clock time
        s.send(pickle.dumps(0))                                         #7,send a 0 to the child so it can terminate
                
        p2.join()                                                       # 8,wait for the child to end
        try: 
            if list1[-1] != 300 and len(list1) != 300:                    #9,verify that the returned data is as expected
                raise ValueError("An error occurred")
        except ValueError:
            print("Data not expected, program will end")
            raise SystemExit
        
        return transfernumber/t                                        #10, return the ratio                
    
if __name__ == '__main__':
    print("OS: "+ platform.system())
    print("Number of cores: "+ str(mp.cpu_count()))
    print("2ProcessQueue: "+ str(highlevel()))
    print("Socket	     : "+ str(lowlevel()))

    print("2ProcessQueue: "+ str(highlevel()))
    print("Socket	     : "+ str(lowlevel()))

    print("2ProcessQueue: "+ str(highlevel()))
    print("Socket	     : "+ str(lowlevel()))
