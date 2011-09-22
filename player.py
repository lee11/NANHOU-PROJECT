import EntityTypes, animation, main

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

#the number of frames that a given transition should last for 
DYING_TIME = 30
GONE_TIME = 10
APPEARING = 30
RESPAWNED =120  

FLICKER_INTERVAL = 10 

#TODO: add state for counterbomb window, bombing


class Player(EntityTypes.Entity):
    DEFAULT_MOVE = 4
    SLOW_MOVE = 2
    shotIntervalTicks = 5
    bulletSpeed = 6
    bulletRadius = 5
    bulletDamage = 5
    def __init__(self, controlState, sprite, pos, points=0):
        super(Player, self).__init__(self, sprite, pos)
        self.controlState = controlState
        self.state = OK
        self.power = 0
        self.lastShot= 0
        #Count the number of frames that you have been in the current state.
        #This will be used to handle the timed transition between several states 
        self.stateTime = 0
        self.dir = 'i'
        self.changedDir = False
    #the move logic calls update dir, and the general update method takes
    #care of changing the animation sprite if necessary
    def updateDir(self, d):
        if d != self.dir:
            self.changedDir = True
            self.dir = d
    def move(self):
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
        self.lastShot += 1
        self.stateTime += 1
        #the animation will reset at the beginning if you set animation
        #to the one you are currently playing
        if self.changedDir: self.animator.setAnimation(self.dir)
        
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

        
    
    def canShoot(self):
        return self.lastShot >= self.shotIntervalTicks
        
    def shoot(self);
        b = []
        b.append(Bullet(self.playerBulletSprite, (self.x, self.y), vel=(0,self.bulletSpeed*-1), radius=self.bulletRadius, damage=self.bulletDamage))
        b.append(Bullet(self.playerBulletSprite, (self.x, self.y), vel=(self.bulletSpeed*-1,self.bulletSpeed*-1), radius=self.bulletRadius, damage=self.bulletDamage))
        b.append(Bullet(self.playerBulletSprite, (self.x, self.y), vel=(self.bulletSpeed,self.bulletSpeed*-1), radius=self.bulletRadius, damage=self.bulletDamage))
        self.lastShot = 0
        return b
    #this method will be called whenever the player has been hit. this should cause the player object
    #to undrgo all of the "dying" effects
     #TODO: add counter bomb timer when bombing is added
     #also, we will want to use a non-looping animation for dying/reapparing, and maybe want to set the state
     #transition to happen at then end of the animation
    def die(self):
        if self.state != OK:
            main.tsprint("PLAYER: Error: die method called when player is not in OK state.")
       
        
        #start playing the dying animation
        #playing dying sound
        #set state to dying
        
