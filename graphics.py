import pygame

#A surface which can be used for intermediary blitting in
#order to draw a sprite with a different alpha.

#Borrowed from: http://www.nerdparadise.com/tech/python/pygame/blitopacity/

alphaTemp = None

def blit_alpha(target, source, location, opacity):
    global alphaTemp
    if alphaTemp == None: alphaTemp = pygame.Surface((640, 480)).convert()
    x,y = location
    alphaTemp = pygame.Surface((source.get_width(), source.get_height())).convert()
    alphaTemp.blit(target, (-x, -y))
    alphaTemp.blit(source, (0, 0))
    alphaTemp.set_alpha(opacity)    
    target.blit(alphaTemp, location)
