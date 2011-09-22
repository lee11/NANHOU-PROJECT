import pygame, threading, thread, time, main


#This function decorator will automatically handle synchromizing functions 
def sync(func):
    @wraps(func)
    def _synched(self, *args, **kwargs):
        self.lock.acquire()
        try:
            return func(self, *args, **kwargs)
        finally:
            self.lock.release()
    return _synched

KEYUP = 0
KEYDOWN = 1
KEYLEFT = 2
KEYRIGHT = 3
KEYSHOT = 4
KEYSLOW = 5
KEYBOMB = 6
KEYPAUSE = 7

class ControlState:
    def __init__(self):
        self.keyup = False 
        self.keydown = False
        self.keyleft = False
        self.keyright = False
        self.keyshot = False
        self.keyslow = False
        self.keybomb = False
        self.keypause = False
    def slowPressed(self):
        return self.keyslow
    def shotPressed(self):
        return self.keyshot
    def bombPressed(self):
        return self.keybomb
    def pausePressed(self):
        return self.keypause
    def upPressed(self):
        return self.keyup and not self.keydown
    def downPressed(self):
        return self.keydown and not self.keyup
    def leftPressed(self):
        return self.keyleft and not self.keyright
    def rightPressed(self):
        return self.keyright and not self.keyleft

    #This method is slower and requires polling, but it solves the problem of keys "sticking" in the down state  
    def readKeyState(self):
        keyList = pygame.key.get_pressed()
        self.keypause = keyList[pygame.K_ESCAPE]
        self.keyup = keyList[pygame.K_UP]
        self.keydown = keyList[pygame.K_DOWN]
        self.keyleft = keyList[pygame.K_LEFT]
        self.keyright = keyList[pygame.K_RIGHT]
        self.keyshot = keyList[pygame.K_z]
        self.keybomb = keyList[pygame.K_x]
        self.keyslow = keyList[pygame.K_LSHIFT]
    def handleKeyPress(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE :
                self.keypause = True
            elif e.key == pygame.K_UP:
                self.keyup = True
            elif e.key == pygame.K_DOWN:
                self.keydown = True
            elif e.key == pygame.K_LEFT:
                self.keyleft = True
            elif e.key == pygame.K_RIGHT:
                self.keyright = True
            elif e.key == pygame.K_z:
                self.keyshot = True
            elif e.key == pygame.K_x:
                self.keybomb = True
            elif e.key == pygame.K_LSHIFT:
                self.keyslow = True
            else:
                main.tsprint ('CONTROL STATE: unrecognized keypress %d' % e.key)
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_ESCAPE :
                self.keypause = False
            elif e.key == pygame.K_UP:
                self.keyup = False
            elif e.key == pygame.K_DOWN:
                self.keydown = False
            elif e.key == pygame.K_LEFT:
                self.keyleft = False
            elif e.key == pygame.K_RIGHT:
                self.keyright = False
            elif e.key == pygame.K_z:
                self.keyshot = True
            elif e.key == pygame.K_x:
                self.keybomb = True
            elif e.key == pygame.KMOD_LSHIFT:
                self.keyslow = True

class EventHandler(object):
    sleepInterval = 0.005
    def __init__(self, eventsSource=pygame.event.get):
        '''
        Creates an object for handling events. the quit notifier is the function that will
        be called when the event handler sees a pygame.quit event. the eventsSource is a 
        functoin that the EventHandler cal poll for a list of new events (by default this
        will be pygame.events.get)
        '''
        self.eventSource = eventsSource
        self.controlState = ControlState()
        self.lock = threading.Lock()
        self.quit = False
        self.handleQuit =False
    def getControlState(self):
        return self.controlState
    def eventCycle(self):
        while not self.quit:
            self.lock.acquire()
            self.handleEvents()
            self.lock.release()
            if self.handleQuit:
            	self.quitNotifier(*self.quitNotifierArguments)
            	self.stopThread()
            	return
            else: time.sleep(self.sleepInterval)
    def handleEvents(self):
        events = self.eventSource()
        for e in events:
            if e.type == pygame.QUIT:
                self.handleQuit = True
            #if e.type == pygame.KEYUP or e.type == pygame.KEYDOWN:
            #   self.controlState.handleKeyPress(e)
            self.controlState.readKeyState()
    def setQuitHandler(self, func, args):
        self.quitNotifier = func
        self.quitNotifierArguments = args
    def startThread(self):
        #in case the thread is being restarted
        #at some point
        self.quit = False
        
    	t = threading.Thread(target=self.eventCycle, args=())
    	t.daemon = True
    	t.start()
        #thread.start_new_thread(self.eventCycle, ())
        main.tsprint( 'EVENT HANDLER: thread started.')
    def stopThread(self):
        main.tsprint( 'EVENT HANDLER: stopping thread...')
        self.lock.acquire()
        self.quit = True
        main.tsprint( 'EVENT HANDLER: thread stopped')
        self.lock.release()
#TO-DO:

#Consider locking for both the controlState and eventHandler. controlState will be shared, but the second
#thread will only be reading the control state information that is stored. 
#Locking may not be necessary for eventHandler.

#An eventhandler for the game may eventually be run in a new thread so it can always handle events in the background
#(this is useful to both the main menu and the engine)
