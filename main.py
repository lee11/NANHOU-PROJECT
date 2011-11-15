#!/usr/bin/python
"""
The main module that runs the danmaku program. In this version, it just does initialization and runs the engine
and level.
"""

import pygame, getopt, engine, player
import EntityTypes, events, sys, threading, Character
import reimu, SoundHandler, animation, io, __builtin__
from functools import wraps

#SOME DEFAULT CONSTANTS
__builtin__.screenW = 640
__builtin__.screenH = 480
__builtin__.playAreaW =320
__builtin__.playAreaH = 640

__builtin__.interfaceTopleft = (320, 0)
__builtin__.interfaceSize = (320, 480)


profiling = False
COLORDEPTH=32
usage = '''
NANHOU PROJECT v0.1.0b.
Usage:

-q - quiet mode. No non-eror information will printed out.
-p - Enable profiling. The next argument must be a path to a file to store profiling data in.
    If it already exists, it must be a text file with write permissions; it will be appended to.
-w - Specify screen width
-h - Specify screen height
-c - Specify a color depth
'''


def quitHandler(engineReference, eventHandler):
    '''quitHandler will be called at the end of the program as well as the
    handler for a pygame.QUIT event. It sound only run once.'''
    if quitHandler.quitting: return
    quitHandler.quitting = True
    io.tsprint('MAIN: quit handler started.')
    engineReference.stopEngine()
    io.tsprint("MAIN: stopping sound and music...")
    SoundHandler.stopAll()
    SoundHandler.stopMusic()
    io.tsprint("MAIN: done")
    pygame.quit()
    if profiling:
        io.tsprint("MAIN: Stopping profiler and getting data....")
        fout = open(quitHandler.profilingDest, 'a+')
        l = yappi.get_stats(yappi.SORTTYPE_TTOTAL,              
            yappi.SORTORDER_DESCENDING,
            yappi.SHOW_ALL)
        yappi.stop()
        if fout:
            for s in l:
                fout.write(s+'\n')
            fout.close()
            io.tsprint("MAIN: Profiling data written.")
        else:
            io.tserr("MAIN ERROR: Error opening file for profiling data")
    io.tsprint("MAIN: Exiting!")

quitHandler.quitting = False

def mainMethod():
    options, args = getopt.getopt(sys.argv[1:], "qp:w:h:c:", ['help'])
    global COLORDEPTH, screenW, screenH, profiling

    if len(args) > 0:
        io.tserr("Unknown arguments:")
        io.tserr(args)
        io.tserr(usage)
        exit()
    for o, a in options:
        if o == '-q': io.tsprint.quietMode = True
        elif o == '-p':
            profiling = True
            import yappi
            io.tsprint('MAIN: Starting YAPPI profiler')
            yappi.start()
            quitHandler.profilingDest = a
        elif o == '-w': screenW = int(a)
        elif o == '-h': screenH = int(a)
        elif o== '--help':
            print usage
            exit()
        elif o=='-c':  COLORDEPTH = int(a)
        
    WINSIZE=(screenW,screenH)
    level = __import__('level')
     
    pygame.init()
    print 'winsize',
    print WINSIZE
    screen = pygame.display.set_mode(WINSIZE,pygame.DOUBLEBUF,COLORDEPTH)
    pygame.display.set_caption("NANHOU PROJECT v0.1.0b")
    
    eventHandler = events.EventHandler()
    __builtin__.currentEngine = engine.Engine(screen,eventHandler.getControlState())
    eventHandler.setQuitHandler(quitHandler, (currentEngine, eventHandler))
    
    #create player and add to engine
    __builtin__.currentPlayer = reimu.PlayerClass(eventHandler.getControlState()) 
    eventHandler.startThread()
    currentEngine.setPlayer(currentPlayer)    
    currentEngine.startEngineThread()    
    
    if not hasattr(level, 'runLevel'):
        io.tserr("MAIN ERROR:, The level module that has been loaded does does not have a runLevel attribute.")
    #:If the engine is stopped before the level script runs to completion (e.g. by the 
    #event handler handling a quit event) the engine will be stopped. Any call to any of the 
    #methods that constitute the level-script interface to the engine will return a LevelOverException
    #which will halt execution of the level
    try:
        level.runLevel()
    except engine.LevelOverException:
        pass
    quitHandler(currentEngine, eventHandler)
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


