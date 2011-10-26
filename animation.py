'''
This module handles loading animations. An animation is a list of sequences of images. An animation should be stored
in a single directory. Each sequence of the animation is described by a prefix and a postfix, either of which may be 
empty strings. Each sequence should consist of files of the form $prefix$n$postfix, where n is a number starting at 0. This module will detect zero-padding for up to five digits, but the padding has to be consistent. Each sequence is uniquely keyed by prefix, postfix, and dirStr. Multiple copies will not be loaded.
'''

import os, os.path, pygame.image, main
import engine, vector

loadedAnimations = {}

mainEngine = None

def getAnimation(prefix, postfix = '.png', dirStr = '.'):
    '''
    Loads an animation object based on prefix, postfix, dirStr as the key.
    A copy will be looked up from the loadedAnimations table if the animation
    has already been loaded. (This should not be called from another module)
    These will be wrapped in an AnimationWrapper to provide per Entity animation drawing.
    '''
    if (prefix, postfix, dirStr) in loadedAnimations:
        return loadedAnimations[(prefix, postfix, dirStr)]
    else:
        loadedAnimations[(prefix, postfix, dirStr)] = Animation (prefix, postfix, dirStr)
        return loadedAnimations[(prefix, postfix, dirStr)]
        
#TO ADD: support for purging animations that haven't been used in a while?

class Animation(object):
    '''
    An Animation contains a sequence of images which will be used for animation
    Use getAnimation instead of the constructor to avoid creating unneccesary copies
    These are "immutable" and will be wrapped in an Animator to provide a per instance animation object. 
    These should not be instaniated outside of getAnimation. 
    '''
    def __init__(self, prefix, postfix = '.png', dirStr = '.'):
        self.images = loadImages(prefix, postfix, dirStr)
        
class AnimationWrapper(object):
    '''
    An AnimationWrapper wraps state around an Animation. This allows for multiple animations whose frames can sequenced
    independently of each other, while using the same images. These should not be instantiated by other modules.
    '''
    def __init__(self, prefix, postfix = '.png', dirStr = '.'):
        self.an = getAnimation(prefix, postfix, dirStr).images
        self.length = len(self.an)
        self.maxIndex = self.length - 1
        self.currentImage = -1
        self.loop = True
        
    def start(self):
        '''
        This will set the animation to the first frame and reset the frame counter. 
        '''
        self.currentImage = -1
        #return self.an[0]
        
    def setLooping(self, value):
        '''
        Set if the animation is to loop or stop on the last frame. "value" is a boolean.
        '''
        self.loop = value
    
    # Get the next frame in the Animation.
    # Changed modulo to if block to increase speed.
    # Added looping toggle.
    def next(self):
        '''
        Move to the next frame in the animation.
        '''
        if self.loop:
            self.currentImage += 1
            if self.currentImage > self.maxIndex:
                self.currentImage = 0
            return self.an[self.currentImage]
        elif currentIndex == self.maxIndex:
            return self.an[self.maxIndex]
        else:
            self.currentImage += 1
            if self.currentImage > self.maxImage:
                self.currentImage = self.maxImage
            return self.an[self.currentImage]
            
    # Get the same frame in the Animation.
    def current(self):
        '''
        Get the current frame of the animation.
        '''
        return self.an[self.currentImage]

class Animator(object):
    '''
    An Animator contains a table of AnimationWrappers, keyed by prefix. The animator must be loaded from animations
    in a single directory sharing the same postfix.
    '''
    def __init__(self, prefixList = ['i', 'u', 'd', 'l', 'r'], postfix = '.png', dirStr = '.'):
        '''
        Load an animator. This will automatically load wrapped animations, one for each prefix in the prefixList.
        The animations in the Animation will be accessed by prefix. 
        '''
        self.animationList = {}
        self.lastKnownPrefix = None
        self.frameInterval = None
        self.startFrame = None
        for prefix in prefixList:
            self.animationList[prefix] = AnimationWrapper(prefix, postfix, dirStr)

    # Set the animation display speed. Lower == faster.
    def setFrameInterval(self, frames):
        '''
        This sets the length of an animation frame in game drawing frames (i.e. the number of game drawing frames that an single frame of the animation will be displayed for). 
        '''
        self.frameInterval = frames
        
    def setAnimation(self, prefix, loop=True):
        '''
        Set a given animation to play, with a given frame interval. By default, it will also start at the first frame and loop continually after completing.
        '''
        if not prefix in self.animationList:
            raise ValueError("Prefix not in animation list.")
        self.lastKnownPrefix = prefix
        self.startFrame = mainEngine.getFrameCount()
        self.animationList[prefix].start()
        
    def setLooping(self, prefix, value):
        '''
        Set if the animation is to loop or stop on the last frame. "value" is a boolean.
        '''
        self.animationList[prefix].setLooping(value)
        
    # Get the next image in an Animation.
    def getCurrentImage(self, frames):
        '''
        Get the current image of the animator.
        '''
        #if self.lastKnownPrefix == None:
        #    main.tsprint("ANIMATION: Trying to get animation without settings animation sequence.")
        #    return
        # Switching images/frames.
        if self.startFrame == None:
            raise AttributeError("Animation has not been set.")
        #print (frames, self.startFrame, self.frameInterval)
        if (frames - self.startFrame) > self.frameInterval:
            self.startFrame = frames
            return self.animationList[self.lastKnownPrefix].next()
        else:
            return self.animationList[self.lastKnownPrefix].current()

# Get a sequence of images based on a prefix and ascending numbering system.
# Example 'u0.png' to 'u5.png'.
#nDigits is total number of digits in the number. e.g. 05 = two digits
#the digit in the sequence will be zero-padded so that it contains nDigits 
#digits

maxDigits = 5

def loadImages(prefix, postfix = '.png', dirStr = '.',):
    '''
    Load a sequence of images that represent an animation.
    '''
    l = []
    i=0
    foundAny = False
    
    #automatically determine the amount of zero padding in the current sequence
    nDigits = 1
    for j in range(maxDigits, 0, -1):
        if os.path.exists(os.path.join(dirStr,prefix + ("%.*d" % (j, 0)) + postfix)):
            nDigits = j
        
    while True:
        itemStr = (prefix + ("%.*d" % (nDigits, i)) + postfix)
        fullPath = os.path.join(dirStr, itemStr)
        if os.path.exists(fullPath):
            l.append(pygame.image.load(fullPath))
            foundAny = True
        else:
            if not foundAny: main.tsprint('ANIMATION: Error, first item %s in animation sequence not found' % itemStr)
            break
        i += 1
    return l
