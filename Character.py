'''
This module handles loading characters. The character class should subtype EntityTypes.Player and it should be called PlayerClass. The module should  include the following fields: portrait, desc, longDesc, 
'''

import pygame.image
   
playerTable = {}

def nameCheck(func):
    '''
    Check to see that name is the table of currently loaded players.
    '''
    def wrapped(name):
        if not n in playerTable:
            raise ValueError('"%s" not in character table.' % (n))
            return
        else: return func(name)
    return wrapped

def getPlayerNames():
    '''
    Return a list of names of the currently loaded characters.
    '''
    return [k for k in playerTable]
    
@nameCheck
def getPlayer(name):
    '''
    Get a new player object by name.
    '''
    return playerTable[name].PlayerClass()

@nameCheck
def getPortrait(name):
    '''
    Get the portrait of the player
    '''
    return playerTable[name].portrait

@nameCheck
def getDesc(name):
    '''
    Get the players short description.
    '''
    return playerTable[name].desc

@nameCheck
def getLongDesc(name):
    '''
    Get the players long description or biography.
    '''
    return playerTable[name].longDesc

