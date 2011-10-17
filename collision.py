def noop(*args):
	pass
		
#if funcA is specificed, this function will be called on any object in listA
#that collides with an object in listB

def drawHitbox(s, area, diag):
    if not diag:
    
        for i in range(s.x - s.radius/2, s.x + s.radius/2):
            for j in range(int(s.y - s.radius/2), int(s.y+s.radius/2)):
                area[(i,j)] = s
    else:
        #draw diagonally; the width of each row is equal to the height of 
        for i in range(s.y - s.radius/2, s.y + s.radius/2):
                pass

def perPixelDisjoint(listA, listB, fA, fB, f, res, diag):
    width, height = res
    #for sparse sets of pixels, this will save some memory. but it may also be slower
    #than using a 2d array
    area = {}
    
def disjoint(listA, listB, fA, fB, f):
    '''This performs a disjoint, brute force collision detection between (not among) two sets of Entity-like objects
    (listA and listB). The objects must support the isCollision() interface. If there is a collision between an object
    in listA and an object in listB, fA will be called with the object from listA as its argument, fB will be called 
    with the object from fB as its argument, and f will be called with object A and object B as its argument. These functoins are optional. They can be replaced with None.  
    '''
    
    if f == None: f = noop
    if fA == None: fA = noop
    if fB ==None: fB = noop
    for a in listA:
	    for b in listB:
		    if a.isCollision(b):
			    fA(a)
			    fB(b)
			    f(a,b)

#fs will be called on each item involved; fd will be called on the pair
#symmetric is false by default (only applied if fd is set: if symmetric, then fd will be called twice for the same pair
#fd(a,b) and fd(b,a)
def single(l, func):
    '''
    Perform a collision check among all objects in list l.
    '''
    for i in ['fs', 'fd']:
        setIfPresent(__dict__, kw, i, noop) 
    setIfPresent(__dic__, kw, 'symmetric', False)
    for i in range(0,len(l)-1):
	    for j in range(0,len(l)-1):
		    if i == j: continue
		    if x.isCollision(y):
			    fs(l[i])
			    fs(l[j])
			    fd(l[i],l[j])
			    if symmetric: fs(l[j], l[i])
