
import pygame, pygame.event, pygame.image, pygame.display
import EntityTypes, threading, main
import sys, time, events, collision
from functools import wraps

#The type defines how the engine will handle the objects. Each object type should subclass
#or support the functionality of its respective type, but the generic type specfically refers 
#to entities that do not fall into any other category.

#if the tuple (etype, etype) is in the table, the corresponding function will be called

enemy = 0
point = 1
ebullet = 2
generic = 3
pbullet = 4
player = 5
typeStr = ['enemy', 'point item', 'player bullet', 'enemy bullet', 'generic entity', 'player']

nTypes = 6

collisionTable = {}
    
def enemyVpBullet(enemy, pBullet):
    enemy.hp -= pBullet.damage
    if enemy.hp <= 0: enemy.expired = True
    pBullet.expired = True
collisionTable[(enemy,pbullet)] = enemyVpBullet

def enemyVplayer(enemy, player):
    if enemy.canDamage == True: player.hit = True
collisionTable[(enemy, player)] = enemyVplayer

def pointVplayer(point, player):
    point.applyItem(player)
collisionTable[(point, player)] = pointVplayer

def eBulletVplayer(ebullet, player):
    if ebullet.damage > 0:
        player.die()
        ebullet.expired = True
collisionTable[ebullet, player] = eBulletVplayer

pauseScreen = pygame.image.load('pausescreen.png')

def checkType(eType):
    if eType <0 or eType >= nTypes:
                tsprint("ENGINE: Invalid Entity type specified")
                raise ValueError("ENGINE: Invalid entity type.")

class LevelOverException(Exception):
    """
    Any call to any of the methods that define the level-script interface to the engine will return
    a LevelOverException and halt execution of the level, if the engine has halted. A level script should not
    try to catch this exception, or at least it should return promptly after catching it.
    """
    pass

#This function decorator will automatically handle synchronizing functions
#for the engine 
def sync(func):
    @wraps(func)
    def _synched(self, *args, **kwargs):
        self.lock.acquire()
        try:
            return func(self, *args, **kwargs)
        finally:
            self.lock.release()
    return _synched

#This decorator will automatically prepend a level over check to functions that 
#will be called by the level script.
def levelOverCheck(func):
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
        checkType(eType)
                
    	main.tsprint('ENGINE: %s added', typeStr[eType])
        self.eList[eType].append(entity)
    @sync
    @levelOverCheck
    def addEntities(self, entity, eType):
        checkType(eType)
         
    	main.tsprint( 'ENGINE: %d %s added' % (len(entity), typeStr[eType]))
        self.eList[eType].extend(entity)
    def __init__(self, screen, controlState, res=(640,480)):
        self.done = False
        self.paused = False
        self.controlState = controlState
        self.fpsFrequency = 0.3
        self.frameCount = 0
        self.fps = 0
        self.fpsStartTicks = pygame.time.get_ticks()
        self.fpsStartFrames = 0
        self.screenWidth, self.screenHeight = res
        self.lastCycle = pygame.time.get_ticks()
        self.screen = screen
        #entity list; one for each type; 
        self.eList = []
        for i in range(0,nTypes):
            self.eList.append([])
        self.lock = threading.Lock()
    def getGameArea(self):
    	return self.screenWidth, self.screenHeight
    def entityCount(self, eType=None):
        if eType == None: return sum([len(l) for l in self.eList]) 
    	else: 
            checkType(eType)
            return len(self.eList[eType])
    def handleFPS(self):
        #There are more accurate ways to handle that, but we don't need to worry about that now.
        if (pygame.time.get_ticks() - self.fpsStartTicks)/1000.0 >=  1.0 / self.fpsFrequency:
            self.fps = (self.frameCount - self.fpsStartFrames) * 1.0 / (pygame.time.get_ticks() - self.fpsStartTicks) * 1000
            self.fpsStartFrames = self.frameCount
            self.fpsStartTicks = pygame.time.get_ticks()
            main.tsprint('ENGINE: fps: %d' % self.fps)
    def startEngineThread(self):
    	t = threading.Thread(target=self.runEngine, args=())
    	t.daemon = False
        #This shouldn't need to be true, but the engine doesn't want to stop for some reason
    	t.start()
        #thread.start_new_thread(self.runEngine, ())
    
    def stopEngine(self):
    	main.tsprint('ENGINE: stopping engine...')
    	skipLock = self.paused
	    
        if not skipLock: self.lock.acquire()
        if self.done:
    	    main.tsprint('ENGINE: Engine is already stopped.')
        else:
    	    self.done = True
    	main.tsprint('ENGINE: stopped')
        if not skipLock: self.lock.release()
   
    def setPlayer(self, p):
        self.setPlayers([p])
   
    @sync
    def setPlayers(self, p):
        self.eList[player] = p
    
    @sync
    def getPlayers(self):
        return self.eList[player]
   
    @sync
    def engineLoop(self):
        #handle control
        
        if self.controlState.slowPressed(): main.tsprint(  'ENGINE: slow pressed')
        if self.controlState.shotPressed(): main.tsprint(  'ENGINE: shot pressed')
        if self.controlState.pausePressed(): main.tsprint(  'ENGINE: pause pressed')
        if self.controlState.bombPressed(): main.tsprint(  'ENGINE: bomb pressed')
        if self.controlState.upPressed(): main.tsprint(  'ENGINE: up pressed')
        if self.controlState.downPressed(): main.tsprint(  'ENGINE: down pressed')
        if self.controlState.leftPressed(): main.tsprint(  'ENGINE: left pressed')
        if self.controlState.rightPressed(): main.tsprint(  'ENGINE: right pressed')
        
        #graphics
        self.draw()
        #edge detection
        for l in self.eList:
            for e in l:
                if e.x < 0:
                    e.leftEdge()
                elif e.x >= self.screenWidth:
                    e.rightEdge()
                if e.y < 0:
                    e.topEdge()
                elif e.y >= self.screenHeight:
                    e.bottomEdge()
                    
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
        
        for e in self.eList[enemy]:
            if e.canShoot():
                self.eList[ebullet].extend(e.shoot())
        for p in self.eList[player]:
            if p.canShoot():
                self.eList[pbullet].extend(p.shoot())
    @levelOverCheck
    def getFrameCount(self):
        return self.frameCount
    @levelOverCheck
    def getGameSeconds(self):
        return self.frameCount * engine.frameLenMillis
    #NOT SYNCED: ONLY CALL FROM MAIN ENGINE LOOP
    def draw(self):
        #only draw once every n frames
        if self.frameCount % Engine.drawInterval != 0 or self.done: return
        self.screen.fill(pygame.Color('black'))
        for l in self.eList:
            drawList(l, self.screen, self.frameCount)
        pygame.display.update()

        
    def runEngine(self):
        '''
        This is the method that represents the thread of the engine running. It
        should not be called directly. startEngineThread will start the engine
        running in another thread.
        '''
        while not self.done:
            while pygame.time.get_ticks() - self.lastCycle < Engine.frameLenMillis and not self.done:
                time.sleep(self.idleSleepInterval)
            self.lastCycle = pygame.time.get_ticks()
            if self.done: return
            
            if self.controlState.pausePressed():
                if self.paused:
                    self.paused = False
                    main.tsprint("ENGINE: Engine broke out of pause loop while paused!?")
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
                self.engineLoop()
            except Exception:
                main.tsprint ("ENGINE: exception:" +  str(sys.exc_info()[:]))
                return
    def sleepSeconds(self, sec):
        self.sleepFrames(self.targetFramerate*sec)
    @levelOverCheck
    def sleepFrames(self, frames):
        end = self.frameCount + frames
        while self.frameCount < end:
            #this way the level will end promptly even if the engine
            #quits while the leve is waiting for a long time
            if self.done:
            	main.tsprint ('ENGINE: engine stopped while level script is sleeping.')
            	main.tsprint ('ENGINE: Sending exception to level...')
            	raise LevelOverException()
            else:
            	time.sleep(self.idleSleepInterval)
         
    def handleReleaseItems(self, l):
        for t in l:
            eType, li = t
            checkType(eType)
            #main.tsprint("ENGINE: %d %ss released" % (len(li), typeStr[eType]))
            self.eList[eType].extend(li)

def drawList(entityList, surface, frame):
    for entity in entityList:
        if entity.opacity <= 0 or entity.animator == None:
            return
        sprite = entity.getCurrentSprite(frame)
        width, height = sprite.get_size()
        if entity.opacity >= 255:
            surface.blit(sprite, (entity.x-width/2, entity.y-height/2))
        else:
            #http://www.nerdparadise.com/tech/python/pygame/blitopacity/
            temp = pygame.Surface((640, 480)).convert()
            temp.blit(surface, (entity.x*-1, entity.y*-1))
            temp.blit(sprite, (0,0))
            temp.set_alpha(entity.opacity)
            surface.blit(temp, (entity.x, entity.y))
            

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
