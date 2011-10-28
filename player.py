import EntityTypes, SoundHandler, animation

#states - these represent the states the player can be in. update() will check to see
#what state the player is in. 

#normal game play
OK = 0
#dying animation - no control
DYING = 1
#sprite is not being drawn to the screen
GONE = 2
#spwaning animation. player is reapparing on the screen
APPEARING = 3
#like OK, except player is flickering and will be invulnerable
RESPAWNED = 4

N_STATES = 5 

#the number of frames that a given transition should last for 

DYING_TIME = 30
GONE_TIME = 120
APPEARING_TIME = 60
RESPAWNED_TIME =120  

FLICKER_INTERVAL = 10

def stateCheck(state):
    if state < 0 or state >= N_STATES:
        raise ValueError("Invalid state value.")

#TODO: add state for counterbomb window, bombing

class Player(EntityTypes.Entity):
    '''
    This class represents a player entity which will be part of the game play.
    '''
    DEFAULT_MOVE = 4
    SLOW_MOVE = 2
    shotIntervalTicks = 5
    bulletSpeed = 6
    bulletRadius = 5
    bulletDamage = 5
    DEFAULT_LIVES = 5
    DEFAULT_BOMBS = 3
    def __init__(self, controlState):
        '''
        Create a player object. The player should not need to be parameterized (a subclass should be created instead).
        The player will need a reference to a ControlState object.
        '''
        super(Player, self).__init__(None, (0,0))
        
        self.score = 0
        self.lives = self.DEFAULT_LIVES
        self.bombs = self.DEFAULT_BOMBS
        self.controlState = controlState
        self.state = OK
        self.power = 0
        self.lastShot= 0
        #This will be set if the player hits anything
        self.hit = False
        #will need to consider how we are setting the different animations
        #self.animations = [None for i in range(0,N_STATES)]
        self.animator = None
        #these are the sounds that will be played when the player 
        #transitions into a given state
        self.transitionSounds = [None for i in range(0,N_STATES)]
        #Count the number of frames that you have been in the current state.
        #This will be used to handle the timed transition between several states 
        self.stateTime = 0
        self.dir = 'i'
        self.changedDir = False
    #the move logic calls update dir, and the general update method takes
    #care of changing the animation sprite if necessary
    
    #this should take a list of tuples, each of which contains the 
    #state followed by the animator to set for that state
    
    def leftEdge(self):
        '''
        Function to be called when the Player touches or passes the left edge.
        '''
        self.x =1
    def rightEdge(self):
        '''
        Function to be called when the Player touches or passes the right edge.
        '''
        self.x = screenW - 1
    def topEdge(self):
        '''
        Function to be called when the Player touches or passes the top edge.
        '''
        self.y = 1
    def bottomEdge(self):
        '''
        Function to be called when the Player touches or passes the bottom edge.
        '''
        self.y = screenH - 1    
    def setSounds(self, tList):
        '''
        Set the transition sound for mutliple states. Each item should be a tuple, the first element of which should be player module state constant, and the second should be a pygame.Sound-like object. The sound will be played when the player transitions into the state.
        '''
        for t in tList:
            self.setSound(t)
    def getCurrentSprite(self, nFrames):
        '''
        Get the current sprite of the player based on the game engine frame count
        '''
        stateCheck(self.state)
        #return self.animations[self.state].getCurrentImage(nFrames)
        #print self.animator.animationList[self.dir].currentImage
        #print self.animator.startFrame
        return self.animator.getCurrentImage(nFrames)
    
    def setAnimations(self, tList):
        '''
        Set the Animator for multiple states. Each item should be a tuple, the first element of which should be player module state constant, and the second should be an Animator object. The animation will be used when the player is in that state.
        '''
        for t in tList:
            self.setAnimation(t)
            
    def setSound(self, state, sound):
        '''
        INTERNAL USE
        '''
        checkState(state)
        self.transitionSounds[state] = SoundHandler.load(sound)
    
    def setAnimation(self, state, animation):
        '''
        INTERNAL USE
        '''
        checkState(state)
        self.animations[state] = animation
    def updateDir(self, newdir):
        '''
        Set the current animation if the new direction is different from the current one.
        '''
        if newdir != self.dir:
            self.changedDir = True
            self.dir = newdir
            
    def move(self):
        '''
        Move player based on controlState information and update animation based on direction of motion.
        '''
        if self.state != OK and self.state != RESPAWNED: return
        noHorizontal, noVertical = False, False
        if self.controlState.slowPressed():
            crntMove = self.SLOW_MOVE
        else:
            crntMove = self.DEFAULT_MOVE
        if self.controlState.upPressed():
            self.y -= crntMove
            self.updateDir('u')
        elif self.controlState.downPressed():
            self.y += crntMove
            self.updateDir('d')
        else:
            noVertical = True
        #this will give priority to left or right animations
        #over up or down animation in the case of diagonal movement 
        if self.controlState.leftPressed():
            self.x -= crntMove
            self.updateDir('l')
        elif self.controlState.rightPressed():
            self.x += crntMove
            self.updateDir('r')
        else:
            noHorizontal = True
        if noHorizontal and noVertical:
            self.updateDir('i')
    def update(self):
        '''
        INTERNAL USE: General updating, include state transitions
        '''
        if self.hit:
            self.hit = False
            if self.state == OK: self.die()

        self.lastShot += 1
        self.stateTime += 1
        #the animation will reset at the beginning if you set animation
        #to the one you are currently playing
        #if self.changedDir: self.animations[self.state].setAnimation(self.dir)
        if self.changedDir:
            self.animator.setAnimation(self.dir)
            self.changedDir = False
        
        if self.state == DYING:
            if self.stateTime >= DYING_TIME:
                self.opacity = 0 #disappear
                self.stateTime = 0
                self.state = GONE
        elif self.state == GONE:
            if self.stateTime >= GONE_TIME:
                self.opacity = 255 #reappear
                self.stateTime = 0
                self.state = APPEARING
        elif self.state == APPEARING:
            #playing reappearing animation
            if self.stateTime >= APPEARING_TIME:
                self.stateTime = 0
                self.state = RESPAWNED
        elif self.state == RESPAWNED:
            if self.stateTime % FLICKER_INTERVAL ==0:
                if self.opacity != 255: self.opacity = 255
                else: self.opacity = 128
            if self.stateTime >= RESPAWNED_TIME:
                self.stateTime = 0
                self.state = OK
        #if self.animations[self.state] == None:
        #    self.doNotDraw = True #will need to add this to EntityTypes
        #else: self.animator = self.animations[self.state]
        if self.animator == None:
            self.doNotDraw = True
        else:
            self.doNotDraw = False
            
    def canShoot(self):
        '''This method returns whether or not the player can shoot'''
        return self.lastShot >= self.shotIntervalTicks and self.controlState.shotPressed() and (self.state == OK or self.state==RESPAWNED)
    def shoot(self):
        '''Return a list of bullets to be fired'''
        return []
    #this method will be called whenever the player has been hit. this should cause the player object
    #to undrgo all of the "dying" effects
     #TODO: add counter bomb timer when bombing is added
     #also, we will want to use a non-looping animation for dying/reapparing, and maybe want to set the state
     #transition to happen at then end of the animation
    def die(self):
        '''Move character to the dying state'''
        if self.state != OK:
            main.tsprint("PLAYER: Error: die method called when player is not in OK state.")
       
        self.state = DYING   
        self.stateTime=0     
