#!/usr/bin/python
"""
The main module that runs the danmaku program. In this version, it just does initialization and runs the engine
and level.
"""

import pygame, pygame.event, pygame.image, pygame.display, engine
import EntityTypes, events, sys, threading, SoundHandler, animation
from functools import wraps
import yappi


#regular print is not threadsafe. Other threads may be printing, so use this
def tsprint(str):
    tsprint.tsprintLock.acquire()
    print str
    tsprint.tsprintLock.release()
tsprint.tsprintLock = threading.Lock()
def quitHandler(engineReference, eventHandler):
    #quitHandler will be called at the end of the program as well as the
    #handler for a pygame.QUIT event. We want to make sure that the quit handler
    #only runs once.
    if quitHandler.quitting: return
    quitHandler.quitting = True
    tsprint('MAIN: quit handler started.')
    engineReference.stopEngine()
    tsprint("MAIN: stopping sound and music...")
    SoundHandler.stopAll()
    SoundHandler.stopMusic()
    tsprint("MAIN: done")
    pygame.quit()
    tsprint("MAIN: Stopping profiler and getting data....")
    fout = open(quitHandler.profilingDest, 'a+')
    l = yappi.get_stats(yappi.SORTTYPE_TTOTAL,              
        yappi.SORTORDER_DESCENDING,
        yappi.SHOW_ALL)
    yappi.stop()
    if fout:
        for s in l:
            fout.write(s+'\n')
        fout.close()
        tsprint("MAIN: Profiling data written.")
    else:
        tsprint("Error opening file for profiling data")
    tsprint("MAIN: Exiting!")

quitHandler.quitting = False

def mainMethod():
    WINSIZE=(640,480)
    COLORDEPTH=32
    quitHandler.profilingDest = 'profile.txt'
    tsprint('MAIN: Starting YAPPI profiler')
    yappi.start()

    level = __import__('level')
    
    ######################################
    #Handle default / keyword parameters
    '''
    if 'WINSIZE' in kwargs: WINSIZE = kwargs['WINSIZE']
    else: WINSIZE = (640,480)
    
    if 'COLORDEPTH' in kwargs: COLORDEPTH = kwargs['COLORDEPTH']
    else: COLORDEPTH = 32
    
    if 'level' in kwargs: level = __import__(kwargs['level'])
    else: level = __import__('level')
    
    if 'profilingDest' in kwargs: profilingDest = kwargs['profilingDest']
    else: profilingDest = 'profile.txt'
    '''    
    pygame.init()
    print 'winsize',
    print WINSIZE
    screen = pygame.display.set_mode(WINSIZE,pygame.DOUBLEBUF,COLORDEPTH)
    pygame.display.set_caption("NANHOU PROJECT v0.1.0a")
    
    eventHandler = events.EventHandler()
    mainEngine = engine.Engine(screen,eventHandler.getControlState(),WINSIZE)
    animation.mainEngine = mainEngine
    eventHandler.setQuitHandler(quitHandler, (mainEngine, eventHandler))
    
    eventHandler.startThread()    
    mainEngine.startEngineThread()    
        
    if not hasattr(level, 'runLevel'):
        tsprint("MAIN: Error:, The level module that has been loaded does does not have a runLevel attribute.")
    #:If the engine is stopped before the level script runs to completion (e.g. by the 
    #event handler handling a quit event) the engine will be stopped. Any call to any of the 
    #methods that constitute the level-script interface to the engine will return a LevelOverException
    #which will halt execution of the level
    try:
        level.runLevel(mainEngine)
    except engine.LevelOverException:
        pass
    quitHandler(mainEngine, eventHandler)
if __name__=="__main__":
    mainMethod()
    
################
#To add:
#
#Support for loading score data into memory on startup.
#
#A menu system (probably state based).
#
#for quitting the program, will need to use stopEngine() to make sure it quits safely and then pickle
#all the score information before quitting.
#
#Consider running the level script in another thread (daemon mode), which wall cause it to quit automatically
# when the main program ends. will also need to consider how to kill it so the current level can be ended without
#it continuing to exist


