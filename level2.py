import EntityTypes, pygame, time, engine

def runLevel(en):
    '''
    Takes a reference to the engine and runs the level
    '''
    f = [Fairy((75, i*20), (-10, 0)) for i in range(0,10)]
    f.extend([Fairy((75, 200-i*20), (10, 0)) for i in range(0,10)])
    en.addEntities(f)
    #en.sleepSeconds(2)
    
    f = [Fairy((75, i*20), (-10, 0)) for i in range(0,1000)]
    f.extend([Fairy((75, 200-i*20), (0, 10)) for i in range(0,100)])
    print en.addEntities(f)
    
 
    
    f = [Fairy((75, i*20), (-10, 0)) for i in range(0,10000)]
    f.extend([Fairy((75, 200-i*20), (0, 10)) for i in range(0,100)])
    en.addEntities(f)
    en.sleepSeconds(12)
        
    
class Fairy(EntityTypes.Entity):
    sprite = pygame.image.load('fairy.png')
    def __init__(self, pos, vel):
        super(Fairy, self).__init__(Fairy.sprite, pos, vel, radius=5)
