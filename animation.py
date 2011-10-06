import os, os.path, pygame.image, main
import engine, vector

loadedAnimations = {}

mainEngine = None

#use prefix, postfix, dirStr as the key
def getAnimation(prefix, postfix = '.png', dirStr = '.'):
    if (prefix, postfix, dirStr) in loadedAnimations:
        return loadedAnimations[(prefix, postfix, dirStr)]
    else:
        loadedAnimations[(prefix, postfix, dirStr)] = Animation (prefix, postfix, dirStr)
        return loadedAnimations[(prefix, postfix, dirStr)]
        
#maybe add support for manually unloading animations that
#are no longer in use?

# An Animation contains a sequence of images which will be used for animation
# it should be a singleton to avoid wasting memory. Use getAnimation instead
#of the constructor to avoid creating unneccesary copies 

class Animation(object):

    def __init__(self, prefix, postfix = '.png', dirStr = '.'):
        self.image = loadImages(prefix, postfix, dirStr)
        self.length = len(self.image)    
        
class AnimationWrapper(object):
    def __init__(self, prefix, postfix = '.png', dirStr = '.'):
        self.an = getAnimation(prefix, postfix, dirStr).image
        self.length = len(self.an)
        self.currentImage = 0
    
    # When switching to this Animation from another,
    # start at the first frame.
    def start(self):
        self.currentImage = -1
        #return self.an[0]
    
    # Get the next frame in the Animation.
    def next(self):
        self.currentImage += 1
        return self.an[self.currentImage % self.length]

    # Get the same frame in the Animation.
    def current(self):
        return self.an[self.currentImage % self.length]

# An Animator contains a dictionary of Animations from which it can retrieve
# an image depending on parameters
class Animator(object):
    
    def __init__(self, prefixList = ['i', 'u', 'd', 'l', 'r'], postfix = '.png', dirStr = '.'):
        self.animationList = {}
        self.lastKnownPrefix = None
        self.frameInterval = None
        self.startFrame = None
        for prefix in prefixList:
            self.animationList[prefix] = AnimationWrapper(prefix, postfix, dirStr)

    # Set the animation display speed. Lower == faster.
    def setFrameInterval(frames):
        self.frameInterval = frames
        
    def setAnimation(self, prefix, frameInterval = 1, index=0, loop=True):
        self.currentFrame = index
	self.frameInterval = frameInterval
        self.lastKnownPrefix = prefix
        self.startFrame = mainEngine.getFrameCount()
        self.animationList[prefix].start()
        
    # Get the next image in an Animation.
    def getCurrentImage(self, frames):
        #if self.lastKnownPrefix == None:
        #    main.tsprint("ANIMATION: Trying to get animation without settings animation sequence.")
        #    return
        # Switching images/frames.
        if frames - self.startFrame > self.frameInterval:
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
