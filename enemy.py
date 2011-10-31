import EntityTypes, pattern, SoundHandler, animation, engine

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

