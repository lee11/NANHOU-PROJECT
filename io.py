import threading, sys

#if not hasattr('io', 'tsprintLock'):
#    print "Loaded the print lock"
#    tsprintLock = threading.Lock()
#if not hasattr('op', 'tserrLock'):
#    tserrLock=threading.Lock()
#    print "loaded the error print lock"

def tsprint(s):
    if 'quietMode' in locals(): return
    #'''This is a thread-safe print. It used instead of regular print. It locks, so be careful for very large prints.'''
#    tsprintLock.acquire()
    sys.stdout.write(str(s))
    sys.stdout.write('\n')
    #tsprintLock.release()
    
def tserr(s):
    #'''
    #Same idea as tsprint, but for stderr.
    #'''
    #tserrLock.acqiure()
    sys.stderr.write(str(s))
    sys.stderr.write('\n')
    #tserrLock.release()
