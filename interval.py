import pattern

'''
A library for generation patterns of entity in space as well as in time; the
patterns are composed of individual patterns called at different points over
time. 

The interval making functions will take an Entity-like class and arguments to the constructor.  
'''

class Interval:
    def expired(self):
        '''Return whether or not the interval has completed releasing everything
        that it is going to release.'''
        return True
    def canEmit(self):
        '''
        Return whether or not anything needs to be emitted
        '''
    
    def emit(self, frameCount):
        '''Emit a list of entities that should be returned at the current time,
        coordinated based on frameCount.
        '''
        return []

class circlesInterval(Interval):
    '''
    An interval that coordinates releasing multiple circles over time.
    Pos can either be a tuple or an Entity-like object. If it is an Entity
    then the position of the Entity will be used for the draw location.
    
    If nCircles is zero, then the interval will continue releasing obejects 
    for an infinite amount of time.
    '''
    
    def update_pos(self):
        if not self.updating_pos:
            return
        self.pos = self.target.x, self.target.y
    
    def update_vel(self):
        if self.follow_velocity:
            self.pattern_velocity = self.target.dx, self.target.dy
    
    def __init__(self, eClass, args, nItems, topAngle, pos, outwardVel, frameInterval, rotation=0, nCircles=None, followVelocity=False, frameCount):
        self.eClass = eClass;
        self.constructor_args = args
        self.items_per_circle = nItems
        self.current_top_angle = topAngle
        if(type(pos) == tuple):
            self.updating_pos = False
            self.pos = pos
        else:
            self.updating_pos = True
            self.target = pos
            self.pos = self.target.x, self.target.y
        self.outward_vel = outwardVel
        self.target_frames = frameInterval
        self.last_frame = frameCount
        self.rotation_vel = rotation
        self.target_circles = nCircles
        self.frame_count = frameCount
        self.follow_velocity = followVelocity
        self.pattern_velocity = (0,0)
        if self.follow_velocity and not updating_pos:
            raise ValueError("Attempt to follow velocity when not following an Entity.")
        
        #To-do: apply emit counting logic
        
        
    def canEmit(self, crnt_frames):
        return crnt_frames - self.self.last_frame >= self.target_frames
        
    def emit(self, crnt_frames):
        self.update_pos(self)
        self.update_vel(self)
        l = []
        while crnt_frames - self.last_frame >= self.target_frames: 
            l.extend(makeCircle(self.eClass, self.constructor_args, self.items_per_circle, self.current_top_angle, self.pos, self.outward_vel))
            self.last_frame += self.target_frames
            self.current_top_angle += self.rotation_vel
            if self.target_circles is not None: self.target_circles -= 1
        return l
