import time

class Timer(object):
    """
    General purpose timer which returns time in seconds.
    """
	def __init__():
		self.startTime = 0
		self.pauseTime = 0
		self.started = False
		self.paused = False
		
	def start(self):
	    self.started = True
	    self.paused = False
	    self.startTime = time.time()
	    
	def stop(self):
	    self.started = False
	    self.paused = False
	    
	def getTime(self):
	    if self.started:
	        if self.paused:
	            return self.pauseTime
	        else:
	            return time.time() - self.startTime
	    return 0
	    
	def pause(self):
	    if self.started and not self.paused:
	        self.paused = True
	        self.pauseTime = time.time() - self.startTime
	        
	def unpause(self):
	    if self.paused:
	        self.paused = False
	        self.startTime = time.time() - self.pauseTime
	        self.pauseTime = 0
	        
	def isStarted(self):
	    return self.started
	    
	def isPaused(self):
	    return self.paused
