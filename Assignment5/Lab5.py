import socket
import time
import multiprocessing as mp
import  platform


def highlevelchild(qsent, qget,e):
    while True:
        num = qsent.get()
        if num == 0:
            break
        num += 1
        qget.put(num)
        e.clear()
    

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
    p = mp.Process(target = highlevelchild, args = (qsent,qget,e))  # 1,create a child process and the data transfer mechanism
    p.start()
   

    num = 1 
    qsent.put(num)
    e.set()
    try: 
        num = qget.get()
        if num != 2:                                    #2, test that the connection is okay
            raise ValueError("An error occurred")
    except ValueError:
        print("Data not expected, program will end")
        raise SystemExit
    
    num = 0                                            # 3,re-initialize the integer 
    transfernumber = 0
    start = time.time()                               # 4,start the timer
    while num < 10000:                                 # 5,loop 10,000 times
        num+=1  
        qsent.put(num)
        transfernumber += 1
        #print("sent"+ str(num)) 
        e.set()
        num = qget.get()
        #print("get " + str(num))
    t = time.time()-start                             #6,record the end clock time
    qsent.put(0)                                      #7,send a 0 to the child so it can terminate
    
    '''
    while not qget.empty():
        num+=1  
        qsent.put(num)
        e.set()
        num = qget.get()        
    '''
    p.join()                                              # 8,wait for the child to end
    try: 
        if num != 10000:                                  #9,verify that the returned data is as expected
            raise CustomError("An error occurred")
    except CustomError:
            pass
    
    return transfernumber/t                                 #10, return the ratio


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
            fromClient = int(conn.recv(1024).decode('utf-8'))  
            if fromClient == 0:
                break                              
            num = fromClient+1
            conn.send(str(num).encode('utf-8'))    

def lowlevel():    
    HOST = 'localhost'
    PORT = 5554    

    with socket.socket() as s :
        p2 = mp.Process(target=lowlevelchild)             # 1,create a child process and the data transfer mechanism
        p2.start()        
        s.connect((HOST, PORT))
        
        num = 1
        transfernumber = 0
        s.send(str(num).encode('utf-8'))
        try: 
            fromServer = int(s.recv(1024).decode('utf-8'))
            if fromServer != 2:                                    #2, test that the connection is okay, There's a exception going on here
                raise ValueError("An error occurred")   
        except ValueError:
            print("Data not expected, program will end")
            raise SystemExit            
        
        num = 0                                                # 3,re-initialize the integer 
        start = time.time()                                        # 4,start the timer
        while num < 10000:                                         # 5,loop 10,000 times
            num += 1
            s.send(str(num).encode('utf-8'))
            transfernumber += 1
            #print("Sent"+str(num))
            num = int(s.recv(512).decode('utf-8'))
            #print("Received from server:", num)
            
        t = time.time()-start       #6,record the end clock time
        s.send(str(0).encode('utf-8'))                                                  #7,send a 0 to the child so it can terminate
                
        p2.join()                                                                          # 8,wait for the child to end
        try: 
            if num != 10000:  
                raise CustomError("An error occurred")
        except CustomError:
                pass
        
        return transfernumber/t                                        #10, return the ratio                
    
if __name__ == '__main__':
    print("OS: "+ platform.system())
    print("Number of cores: "+ str(mp.cpu_count()))
    print("2ProcessQueue: "+ str(highlevel()))
    print("Socket	     : "+ str(lowlevel()))

    print("2ProcessQueue: "+ str(highlevel()))
    print("Socket	     : "+ str(highlevel()))

    print("2ProcessQueue: "+ str(highlevel()))
    print("Socket	     : "+ str(highlevel()))
    