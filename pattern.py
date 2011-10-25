import math

'''
A library for generation patterns of entities. This library can only create patterns in space. It has to be coordinated using Pattern Interval to make patterns that are coordinated over space and time.

The pattern making functions will take an Entity-like class and arguments to the constructor.  
'''

def makeCircle(eClass, args, nItems, topAngle, pos, outwardVel, patternVelocity = (0,0)):
    delta = 2*math.pi / nItems
    angles = [x*delta+topAngle for x in range(0,nItems)]
    entities = []
    dx, dy = patternVelocity
    for a in angles:
        e = eClass(*args)
        e.setPolarVel(outwardVel, a) 
        e.x, e.y = pos
        e.dx += dx
        e.dy += dy
        entities.append(e)
    return entities
