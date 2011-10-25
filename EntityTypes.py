import pygame, vector, math
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
        self.doNotDraw = False
        #radius defines the size of hit-circle for the purposes of collision detection
        self.radius = radius
        #animation will change based on which direction the entity is moving in
        self.curdir = vector.getDirectionPrefix(self.dx,self.dy)
        
        self.animator = animator
        if animator is not None: self.animator.setAnimation('i')
        self.opacity = 255
        ################################
        #To add:
        #rotation - for specifying the rotation of the sprite
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
    def draw(self, frame, surface):
        '''Draw the current frame of animation to a give surface'''
        if self.opacity <= 0 or not self.animator or self.doNotDraw:
            return
        sprite = self.getCurrentSprite(frame)
        width, height = sprite.get_size()
        if self.opacity >= 255:
            surface.blit(sprite, (self.x-width/2, self.y-height/2))
        else:
            #http://www.nerdparadise.com/tech/python/pygame/blitopacity/
            temp = pygame.Surface((640, 480)).convert()
            temp.blit(surface, (self.x*-1, self.y*-1))
            temp.blit(sprite, (0,0))
            temp.set_alpha(self.opacity)
            surface.blit(temp, (self.x, self.y))
        
        newdir = vector.getDirectionPrefix(self.dx,self.dy)
            
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
        '''Get the distance to a Cartiesial position tuple.'''
        x, y, = pos
        return ((self.x - x)**2 + (self.y - y) **2)**0.5
    def release(self):
        '''This will be called after the object has been expired, right before it is removed from gameplay.
        It should return a list of tuples, where the first entry of each tuple is an engine type constant (e.g. engine.POINT) and the second is a list of items of this type to be added 
        to the game'''
        return []
    def setPolarVel(self, r, theta):
        '''Set the polar velocity of an Entity'''
        self.dx = r*math.cos(theta)
        self.dy = r*math.sin(theta)
class Enemy(Entity):
    def __init__(self, animator, hp, pos, vel=(0,0), accel=(0,0), radius=0):
        super(Enemy, self).__init__(animator, pos, vel, accel, radius)
        #Whether or not this object is capable of killing the player on touch
        self.canDamage = True
        #Decremented based on damage
        self.hp = hp
    def canShoot(self):
        '''This will be polled to determine if the object is ready to shoot''' 
        return False
        def shoot(self):
            '''This should return a list of bullets that will be added to gameplay'''
            return []
class Bullet(Entity):
    def __init__(self, animator, pos, vel=(0,0), accel=(0,0), radius=0, damage=1):
        super(Bullet, self).__init__(animator, pos, vel, accel, radius)
        #The amount of damage a bullet is capable of doing. For enemy bullets, any
        #value that evaluates to True means the bullet will kill the player on contact
        self.damage = damage



def nullItem(p, value):
    pass         
def oneUp(p, value):
    p.lives += vlaue
def point(p, value):
    p.points += value
def bombs(p, value):
    p.bombs += value
def power(p, value):
    p.power += value        


class PointItem(Entity):
    NULL=0
    ONEUP=1
    POINT=2
    BOMB=3
    POWER=4
    N_TYPES = 5
    itemTable = [nullItem, oneUp, point, bombs, power]
    def __init__(self, animator, pos, vel=(0,0), accel=(0,0), radius=0, pType=NULL, value=0):
        super(PointItem, self).__init__(animator, pos, vel, accel, radius)
        if pType < 0 or pType >= PointItem.N_TYPES:
            raise ValueError("Invalid PointItem type.") 
        self.type = pType
        self.value = value
    def applyItem(self, player):
        #by default, applyItem will apply the effect of the point item for one of the default types
        #a subtype can override applyItem to make it have a different effect
        PointItem[self.type](player, self.value)
