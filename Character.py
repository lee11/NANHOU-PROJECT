import pygame.image
   
playerTable = {}

def sync(func):
    @wraps(func)
    def wrapped(name):
        if not n in playerTable:
            raise ValueError('"%s" not in character table.' % (n))
            return
        else: return func(name)
    return wrapped

def getPlayerNames():
    return [k for k in playerTable]
    
@nameCheck
def getPlayer(name):
    return playerTable[name].PlayerClass()

@nameCheck
def getPortrait(name):
    return playerTable[name].portrait

@nameCheck
def getDesc(name):
    return playerTable[name].desc

@nameCheck
def getLongDesc(name):
    return playerTable[name].longDesc

