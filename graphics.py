import pygame

pygame.font.init()
FONTSIZE = 24
FONT = pygame.font.Font("FreeMono.ttf", FONTSIZE)

#A surface which can be used for intermediary blitting in
#order to draw a sprite with a different alpha.

#Borrowed from: http://www.nerdparadise.com/tech/python/pygame/blitopacity/

alphaTemp = None

def blit_alpha(target, source, location, opacity):
    global alphaTemp
    if alphaTemp == None: alphaTemp = pygame.Surface((screenW, screenH)).convert()
    x,y = location
    alphaTemp = pygame.Surface((source.get_width(), source.get_height())).convert()
    alphaTemp.blit(target, (-x, -y))
    alphaTemp.blit(source, (0, 0))
    alphaTemp.set_alpha(opacity)    
    target.blit(alphaTemp, location)
    
def blit_text(target, pos, text, color=(255,255,255), opacity = 255):
    blit_alpha(FONT.render(text, True, color), target, pos, opacity)
