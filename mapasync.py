import threading 

#==============================================================================
# Simulates built-in `map` function. Each call is asynchronous
# using thread pool with variable number of thread	
#==============================================================================

def map_async(function, args, options=None, threads=4):
    
    def wrap():
        while(1):
            try:
                lock.acquire()
                param = args_copy.pop()
            except:
                return
            finally:
                lock.release()
                
            result = function(param,options)
            
            try:
                lock.acquire()
                param = res.append(result)
            except:
                return
            finally:
                lock.release()

    lock = threading.Lock()
    args_copy = list(args)
    threads = [threading.Thread(target=wrap) for i in range(threads)]
    res = []
    
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    return list(reversed(res))
    
