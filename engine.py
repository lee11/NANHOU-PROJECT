import pygame
import EntityTypes, threading, io
import sys, time, events, collision, player, traceback
from functools import wraps


'''
The engine handles control, drawing, motion, collision and edge detection. The engine handles constants and methods for interacting with an engine. 
'''

#The type defines how the engine will handle the objects. Each object type should subclass
#or support the functionality of its respective type, but the generic type specfically refers 
#to entities that do not fall into any other category.

#if the tuple (etype, etype) is in the table, the corresponding function will be called

enemyType = 0
point = 1
ebullet = 2
generic = 3
pbullet = 4
playerType = 5
typeStr = ['enemy', 'point item', 'player bullet', 'enemy bullet', 'generic entity', 'player']

nTypes = 6

collisionTable = {}

#Draws a number of icons to represent a given quantity
def drawQuantity(self):
    pass

#Draw the whole interface
def drawInterface(self):
    pass
    
def enemyVpBullet(enemy, pBullet):
    enemy.hp -= pBullet.damage
    if enemy.hp <= 0: enemy.expired = True
    pBullet.expired = True
collisionTable[(enemyType,pbullet)] = enemyVpBullet

def enemyVplayer(enemy, playerEntity):
    if enemy.canDamage == True and playerEntity.state==player.OK: playerEntity.hit = True
collisionTable[(enemyType, playerType)] = enemyVplayer

def pointVplayer(point, playerEntity):
    if playerEntity.state != player.GONE: point.applyItem(playerEntity)
collisionTable[(point, playerType)] = pointVplayer

def eBulletVplayer(ebullet, playerEntity):
    if ebullet.damage > 0 and playerEntity.state ==player.OK:
        playerEntity.hit = True
        ebullet.expired = True
collisionTable[ebullet, playerType] = eBulletVplayer

pauseScreen = pygame.image.load('pausescreen.png')

def checkType(eType):
    if eType <0 or eType >= nTypes:
                raise ValueError("ENGINE: Invalid entity type.")

class LevelOverException(Exception):
    '''
    Any call to any of the methods that define the level-script interface to the engine will return
    a LevelOverException and halt execution of the level, if the engine has halted. A level script should not
    try to catch this exception, or at least it should return promptly after catching it.
    '''
    pass


def sync(func):
    '''This function decorator will automatically handle synchronizing functions for the engine
    This function wrapper engages a NON-REENTRANT lock at the beginning of the function call'''
    @wraps(func)
    def _synched(self, *args, **kwargs):
        self.lock.acquire()
        try:
            return func(self, *args, **kwargs)
        finally:
            self.lock.release()
    return _synched

def levelOverCheck(func):
    '''This decorator will automatically prepend a level over check to functions that 
will be called by the level script.'''
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        if self.done:
            raise LevelOverException()
            return
        else:
            return func(self, *args, **kwargs)
    return wrapped


class Engine():
    #currently these are class field, rather than instance, but that could be changeable.
    #anything that needs to be persistent between engines will need to be class or an external object
    
    '''
    The engine handles control, drawing, motion, collision and edge detection. The engine is thread-safe
    for methods that are part of the level script interface (locking is handled automatically when the 
    method is called. An single instance only supports being started and run once.
    '''
    idleSleepInterval = 1e-3 #seconds
    targetFramerate = 60
    frameLenMillis = 1.0/targetFramerate*1000
    drawInterval = 1 #the ratio of game logic cycles to game draw cycles. 
    pauseSleepInterval = 0.02
    
    

    @levelOverCheck
    @sync
    def addEntity(self, entity, eType):
        '''append the entity of type eType''' 
        checkType(eType)
                
    	io.tsprint('ENGINE: %s added', typeStr[eType])
        self.eList[eType].append(entity)
    @sync
    @levelOverCheck
    def addEntities(self, entity, eType):
        '''append the entities in the entity list of type eType''' 
        checkType(eType)
         
    	io.tsprint( 'ENGINE: %d %s added' % (len(entity), typeStr[eType]))
        self.eList[eType].extend(entity)
    def __init__(self, screen, controlState):
        self.done = False
        self.paused = False
        self.controlState = controlState
        self.fpsFrequency = 0.3
        self.frameCount = 0
        self.fps = 0
        self.fpsStartTicks = pygame.time.get_ticks()
        self.fpsStartFrames = 0
        self.lastCycle = pygame.time.get_ticks()
        self.screen = screen
        #entity list; one for each type; 
        self.eList = []
        for i in range(0,nTypes):
            self.eList.append([])
        self.lock = threading.Lock()
    def entityCount(self, eType=None):
        '''Return the conut of a type of entities in the game, or the sum of all types if no
        type is specified.'''
        if eType == None: return sum([len(l) for l in self.eList]) 
    	else: 
            checkType(eType)
            return len(self.eList[eType])
    def handleFPS(self):
        '''Update logic for determining FPS.'''
        #There are more accurate ways to handle that, but we don't need to worry about that now.
        if (pygame.time.get_ticks() - self.fpsStartTicks)/1000.0 >=  1.0 / self.fpsFrequency:
            self.fps = (self.frameCount - self.fpsStartFrames) * 1.0 / (pygame.time.get_ticks() - self.fpsStartTicks) * 1000
            self.fpsStartFrames = self.frameCount
            self.fpsStartTicks = pygame.time.get_ticks()
            io.tsprint('ENGINE: fps: %d' % self.fps)
    def startEngineThread(self):
        '''This will start the engine in its own thread.'''
    	t = threading.Thread(target=self.runEngine, args=())
    	t.daemon = False
        t.start()
        #thread.start_new_thread(self.runEngine, ())
    
    def stopEngine(self):
        '''This will let the engine finish its current frame and then stop the engine.'''
    	io.tsprint('ENGINE: stopping engine...')
    	skipLock = self.paused
	    
        if not skipLock: self.lock.acquire()
        if self.done:
    	    io.tsprint('ENGINE: Engine is already stopped.')
        else:
    	    self.done = True
    	io.tsprint('ENGINE: stopped')
        if not skipLock: self.lock.release()
   
    def setPlayer(self, p):
        '''Set a single player'''
        self.setPlayers([p])
   
    @sync
    def setPlayers(self, p):
        '''Set a list of players'''
        self.eList[playerType] = p
    
    @sync
    def getPlayers(self):
        '''get the list of players'''
        return self.eList[playerType]
   
    @sync
    def engineLoop(self):
        '''The main loop of engine logic'''
        #handle control
        
        #if self.controlState.slowPressed(): main.tsprint(  'ENGINE: slow pressed')
        #if self.controlState.shotPressed(): main.tsprint(  'ENGINE: shot pressed')
        #if self.controlState.pausePressed(): main.tsprint(  'ENGINE: pause pressed')
        #if self.controlState.bombPressed(): main.tsprint(  'ENGINE: bomb pressed')
        #if self.controlState.upPressed(): main.tsprint(  'ENGINE: up pressed')
        #if self.controlState.downPressed(): main.tsprint(  'ENGINE: down pressed')
        #if self.controlState.leftPressed(): main.tsprint(  'ENGINE: left pressed')
        #if self.controlState.rightPressed(): main.tsprint(  'ENGINE: right pressed')
        
        #graphics
        self.draw()
        #edge detection
        for l in self.eList:
            for e in l:
                if e.x < 0:
                    e.leftEdge()
                elif e.x >= playAreaW:
                    e.rightEdge()
                if e.y >= playAreaH:
                    e.bottomEdge()
                elif e.y < 0:
                    e.topEdge()
                    
        #collision detection
        
        for pair in collisionTable:
            typeA, typeB = pair
            collision.disjoint(self.eList[typeA], self.eList[typeB], None, None, collisionTable[pair])
        
        
        #update
        
        for l in self.eList:
            for e in l:
                e.update()
                    
        #release expired    
        for l in self.eList:
            for e in filter(isExpired, l):
                self.handleReleaseItems(e.release())
                
        #remove expired
        #not pythonic but int indexing is required since list is being modified
        for i in range(0,nTypes):
            self.eList[i] = [e for e in self.eList[i] if not e.expired]
        
        #move items
        
        for l in self.eList:
            for e in l:
                e.move()
        self.frameCount += 1
        self.handleFPS()
        
        #shoot
        
        for e in self.eList[enemyType]:
            if e.canShoot():
                self.eList[ebullet].extend(e.shoot())
        for p in self.eList[playerType]:
            if p.canShoot():
                self.eList[pbullet].extend(p.shoot())
    def getFrameCount(self):
        '''Number of frames the engine has completed.'''
        return self.frameCount
    def getGameSeconds(self):
        '''Number of seconds the engine has been running for.'''
        return self.frameCount * engine.frameLenMillis
    #NOT SYNCED: ONLY CALL FROM MAIN ENGINE LOOP
    def draw(self):
        '''Draw everything'''
        #only draw once every n frames
        if self.frameCount % Engine.drawInterval != 0 or self.done: return
        self.screen.fill(pygame.Color('black'))
        for l in self.eList:
            drawList(l, self.screen, self.frameCount)
        pygame.display.update()

        
    def runEngine(self):
        '''
        This is the method that represents the thread of the engine running. It
        should not be called directly outside of startEngineThread. startEngineThread will start the engine
        in another thread.
        '''
        while not self.done:
            while pygame.time.get_ticks() - self.lastCycle < Engine.frameLenMillis and not self.done:
                time.sleep(self.idleSleepInterval)
            self.lastCycle = pygame.time.get_ticks()
            if self.done: return
            
            if self.controlState.pausePressed():
                if self.paused:
                    self.paused = False
                    io.tserr("ENGINE ERROR: Engine broke out of pause loop while paused!?")
                else:
                    self.paused = True
                    #draw screen and wait for unpause
                    self.screen.fill(pygame.Color('black'))
                    self.screen.blit(pauseScreen, (0, 0))
                    pygame.display.update()
                    #wait for the pause key to be released before polling for its press
                    #to prevent the pause state from changing twice with one press
                    self.lock.acquire()
                    while self.controlState.pausePressed(): time.sleep(0.001)
                    while not self.controlState.pausePressed() and not self.done:
                        time.sleep(self.pauseSleepInterval)
                    while self.controlState.pausePressed(): time.sleep(0.001)
                    self.lock.release()
                    self.paused = False
                    
                    #rather than trying to be smart about timing information while the engine is paused, 
                    #for now we can just flush the FPS information on leaving pause to maintain accuracy
                    self.fpsStartFrames = self.frameCount
                    self.fpsStartTicks = pygame.time.get_ticks()
            if self.done: return
            
            try:
                traceback.extract_tb(self.engineLoop())
            except Exception:
                traceback.print_tb(sys.exc_info()[2])
                io.tserr("ENGINE: exception caught:")
                io.tserr(sys.exc_info()[:])
                return
    def sleepSeconds(self, sec):
        '''Anything calling this method will block for sec ingame seconds and receive a LevelOverException if the engine is stopped before the time is up..'''
        self.sleepFrames(self.targetFramerate*sec)
    @levelOverCheck
    def sleepFrames(self, frames):
        '''Anything calling this method will block for a given number of engine frames and receive a LevelOverException if the engine is stopped before the time is up..'''

        end = self.frameCount + frames
        while self.frameCount < end:
            #this way the level will end promptly even if the engine
            #quits while the leve is waiting for a long time
            if self.done:
            	io.tsprint ('ENGINE: engine stopped while level script is sleeping.')
            	io.tsprint ('ENGINE: Sending exception to level...')
            	raise LevelOverException()
            else:
            	time.sleep(self.idleSleepInterval)
         
    def handleReleaseItems(self, l):
        '''
            INTERNAL USE - add release items from entities in l
        '''
        for t in l:
            eType, li = t
            checkType(eType)
            #main.tsprint("ENGINE: %d %ss released" % (len(li), typeStr[eType]))
            self.eList[eType].extend(li)

def drawList(entityList, surface, frame):
    '''Draw a list of entities'''
    for entity in entityList:
        entity.draw(frame, surface)
            

def isNotExpired(l):
    return not l.expired
    
def isExpired(l):
    return l.expired
    


    
############################
#To add:
# Timed execution queue: add methods to a queue to automatically be run 
# in a given amount of time or at regular intervals
#
#Holding game information, like score/progress
#
#add a way to get a reference to the player
#
#add a way to get references to entities by range/distance
