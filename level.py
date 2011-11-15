import engine, random, animation, SoundHandler,animation, pattern, enemy

def getVel():
    x, y = random.randrange(-2, 2, 1), random.randrange(-2, 2, 1)
    if x==0: x = 1
    if y==0: y = 1
    return x,y

def runLevel():
    SoundHandler.playMusic('un owen.wav')
    '''
    Takes a reference to the engine and runs the level
    '''
    
    f = [enemy.Fairy((250, 200), getVel()) for i in range(0,5)]
    f.extend([enemy.Fairy((75, 200-i*20), getVel()) for i in range(0,10)])
    currentEngine.addEntities(f, engine.enemyType)
    
    f = [enemy.Fairy((75, i*20), getVel()) for i in range(0,10)]
    currentEngine.addEntities(f, engine.enemyType)
    
    for i in range(10):
    
        while currentEngine.entityCount(engine.enemyType) > 5:
            currentEngine.sleepSeconds(1)
        f = [enemy.Fairy((75, i*20), getVel()) for i in range(0,15)]
        currentEngine.addEntities(f, engine.enemyType)
    
    

