import pygame.mixer

pygame.mixer.init()

soundTable = {}
def load(file):
    if file in soundTable:
        return soundTable[file]
    else:
        soundTable[file] = pygame.mixer.Sound(file)
        return soundTable[file]
def pauseAll():
    pygame.mixer.pause()
    pygame.mixer.music.pause()
def unpauseAll():
    pygame.mixer.unpause()
    pygame.mixer.music.unpause()
def stopAll():
    pygame.mixer.stop()
    
def play(sound, volume):
    #todo: set volume for sound effects based on game setting
    sound.set_volume(volume)
    sound.play()
def playMusic(f):
    #todo: set volume for music based on game setting
    pygame.mixer.music.load(f)
    pygame.mixer.music.set_volume(1.0)
    #automatically loop music
    pygame.mixer.music.play(-1)
def stopMusic():
    pygame.mixer.music.stop()
        
#Will need to add strategy for handling large number of sounds trying to play
#(i.e. queue them, drop new or old ones trying to play. We may need to assign a priority
#to special game sounds


