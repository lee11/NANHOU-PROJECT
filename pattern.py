#the pattern making functions will take a function and its arguments; this
#function will be called multiple time and the objects it returns will be used 
#in the pattern

import math
'''
def makeCircle(eClass, args, nItems, topAngle, pos, outwardVel):
    delta = 2*math.pi / nItems
    angles = [x*delta+topAngle for x in range(0,nItems)]
    entities = []
    for a in angles:
        e = eClass.__init__(args)
        e.setPolarVel(outwardVel, a) 
        e.x, e.y = pos
        entities.append(e)
'''
