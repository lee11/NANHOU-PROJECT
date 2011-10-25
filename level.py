import EntityTypes, pygame, time, engine, random, SoundHandler, main, animation, pattern

def getVel():
    x, y = random.randrange(-2, 2, 1), random.randrange(-2, 2, 1)
    if x==0: x = 1
    if y==0: y = 1
    return x,y

def runLevel(en):
    SoundHandler.playMusic('un owen.wav')
    '''
    Takes a reference to the engine and runs the level
    '''
    
    
    Fairy.maxx, Fairy.maxy = en.getGameArea()
    FairyBullet.maxx, FairyBullet.maxy = en.getGameArea()
    f = [Fairy((250, 200), getVel()) for i in range(0,5)]
    f.extend([Fairy((75, 200-i*20), getVel()) for i in range(0,10)])
    en.addEntities(f, engine.enemyType)
    
    f = [Fairy((75, i*20), getVel()) for i in range(0,10)]
    en.addEntities(f, engine.enemyType)
    
    for i in range(100):
    
        while en.entityCount(engine.enemyType) > 5:
            en.sleepSeconds(1)
        f = [Fairy((75, i*20), getVel()) for i in range(0,15)]
        en.addEntities(f, engine.enemyType)
    
    
class Fairy(EntityTypes.Enemy):
    sound = SoundHandler.load('laser.wav')
    sound.set_volume(1)
    def __init__(self, pos, vel):
        self.hasReleased = False
        self.tick = 0
        self.canDamage=1
        super(Fairy, self).__init__(animation.Animator(dirStr="./fairyanim"), 0, pos, vel, radius=30)
    
    def release(self):
        
        #must be a list of tuples each containing the type and list to add 
        #Fairy.sound.play()
        p = pattern.makeCircle(FairyBullet, (((0,0),(0,0))), 10, 0, (self.x, self.y), 2 )
        return [(engine.ebullet, p,)]
#return [(engine.ebullet, [FairyBullet((self.x, self.y), (self.dx*-3, self.dy*-3)) for i in range(0,3)])]
        
class FairyBullet(EntityTypes.Bullet):
    def __init__(self, pos, vel=(0,0), accel=(0,0), radius=10):
        self.richCounter = 0
        super(FairyBullet, self).__init__(animation.Animator(dirStr="./fairybulletanim"), pos, vel, radius=5) 
    def leftEdge(self):
        self.richCounter += 1
        if self.richCounter <=5 :
            if self.x < 0: self.x = 1
            if self.dx < 0: self.dx *= -1
        else: self.expired = True
    def rightEdge(self):
        self.richCounter += 1
        if self.richCounter <=5 :    
            if self.x >= self.maxx: self.x = self.maxx -1
            if self.dx > 0: self.dx *= -1
        else: self.expired = True
    def topEdge(self):
        self.richCounter += 1
        if self.richCounter <= 5:
            if self.y < 0: self.y = 0
            if self.dy < 0: self.dy *= -1
        else: self.expired = True
    def bottomEdge(self):
        self.richCounter += 1
        if self.richCounter <= 5:
            if self.y >= self.maxy: self.y = self.maxy - 1
            if self.dy > 0: self.dy *= -1
        self.expired = True
