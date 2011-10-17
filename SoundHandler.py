import pygame.mixer

pygame.mixer.init()

soundTable = {}
def load(file):
    '''
    Load a sound file, or return a cached copy.
    '''
    if file in soundTable:
        return soundTable[file]
    else:
        soundTable[file] = pygame.mixer.Sound(file)
        return soundTable[file]
def pauseAll():
    '''
    Pause all sounds, including the current music
    '''
    pygame.mixer.pause()
    pygame.mixer.music.pause()
def unpauseAll():
    '''
    Resume all sounds, including the current music.
    '''
    pygame.mixer.unpause()
    pygame.mixer.music.unpause()
def stopAll():
    '''
    Stop all sounds that are playing.
    '''
    pygame.mixer.stop()
def play(sound, volume):
    '''
    Play a sound
    '''
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


