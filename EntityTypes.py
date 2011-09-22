import pygame, animation

class Entity(object):
    '''
    An object that exists in 2D game space and may be drawable to the screen. The edge methods define
    the behaviour of the object upon hitting one of the four edges. The default behaviour is to 
    expire the object. 
    '''
    def __init__(self, animator, pos, vel=(0,0), accel=(0,0), radius=0):
        #Flags the object for removal from the game
        self.expired = False
        self.x, self.y = pos
        self.dx, self.dy = vel
        self.ddx, self.ddy = accel
        #radius defines the size of hit-circle for the purposes of collision detection
        self.radius = radius
        #animation will change based on which direction the entity is moving in
        self.curdir = animation.getDirectionPrefix(self.dx,self.dy)
        
        #currently this is only an SDL surface (bitmap image). Entity will eventually support hold an
        #animator object which will support animaiton
        self.animator = animator
        self.animator.setAnimation('i')
        self.opacity = 255
        ################################
        #To add:
        #rotation - for specifying the rotation of the sprite
        #replace sprite with animator to support animation
        #allow for the use of polar velocity / acceleration as
        #well as rectangular
        ################################
        
    def move(self):
        '''
        This method defines movement (changing the position) of an Entity. Any class that
        overrides this method should also call the original version if the class uses the built-in
        velocity or acceleration.
        '''
        self.dx += self.ddx
        self.dy += self.ddy
        self.x += self.dx
        self.y += self.dy
    def update(self):
        '''
        This is the method where any special logic will be run once per frame to update the entity.
        Any subtype that overrides this method should call the super version so that animation still handled
        correctly
        '''
        
        #The animation will reset at the beginning if it 
        
        newdir = animation.getDirectionPrefix(self.dx,self.dy)
            
        if self.curdir != newdir:
            self.curdir = newdir
            self.animator.setAnimation(newdir)
    def getCurrentSprite(self, nFrames):
        return self.animator.getCurrentImage(nFrames)
    def leftEdge(self):
        self.expired = True
    def rightEdge(self):
        self.expired = True
    def topEdge(self):
        self.expired = True
    def bottomEdge(self):
        self.expired = True
    def isCollision(self, other):
        return (self.radius+other.radius)**2 > (self.x-other.x)**2+(self.y-other.y)**2
    def getDistance(self, pos):
        x, y, = pos
        return ((self.x - x)**2 + (self.y - y) **2)**0.5
    #This will be called after the object has been expired, when it is removed from gameplay.
    #It should return a list of tuples, where the first entry of each tuple is a type as defined
    #in engine (e.g. engine.POINT) and the second is a list of items of this type to be added 
    #to the game
    def release(self):
        return []
    def setPolarVel(self, r, theta):
        self.dx = r*cos(theta)
        self.dy = r*sin(theta)
class Enemy(Entity):
    def __init__(self, animator, hp, pos, vel=(0,0), accel=(0,0), radius=0):
        super(Enemy, self).__init__(animator, pos, vel, accel, radius)
        #Whether or not this object is capable of killing the player on touch
        self.canDamage = True
        #Decremented based on damage
        self.hp = hp
    #Will be polled to determine if the object is ready to shoot    
    def canShoot(self):
        return False
    #Should return a list of bullets that will be added to gameplay
    def shoot(self):
        return []
class Bullet(Entity):
    def __init__(self, animator, pos, vel=(0,0), accel=(0,0), radius=0, damage=1):
        super(Bullet, self).__init__(animator, pos, vel, accel, radius)
        #The amount of damage a bullet is capable of doing. For enemy bullets, any
        #value that evaluates to True means the bullet will kill the player on contact
        self.damage = damage
        
