import pygame
import graphics
import events

SCREEN = None

class Menu(object):
    """
    A menu arbiter.
    """
    def __init__(self, screen):
        self.currentMenu = MainMenu()
        global SCREEN
        SCREEN = screen
    
    def handlekeys(self, keystate):
        self.currentMenu = self.currentMenu.handlekeys(keystate)
    
    def display(self):
        self.currentMenu.display()
    
class MainMenu(object):
    def __init__(self):
        self.prevMenu = self
        self.options = ["Start", "Options", "Quit"]
        self.maxSelection = len(self.options) - 1
        self.selection = 0
        self.states = [StartMenu(self), OptionsMenu(self), Quit(self)]
        
    def handlekeys(self, keystate):
        # Accept option key
        if keystate.shotPressed():
            return self.states[self.selection]
        # Decline option key
        if keystate.bombPressed():
            if self.selection == self.maxSelection:
                return self.states[self.maxSelection]
            else:
                self.selection = self.maxSelection
        # Navigation keys
        if keystate.downPressed():
            self.selection += 1
            if self.selection > self.maxSelection:
                self.selection = 0
        if keystate.upPressed():
            self.selection -= 1
            if self.selection < 0:
                self.selection = self.maxSelection
        # Default return
        return self
        
    def display(self):
        for i in range(len(self.options)):
            if i == self.selection:
                graphics.blit_text(SCREEN, (20, 20 + i * 30), self.options[i])
            else:
                graphics.blit_text(SCREEN, (20, 20 + i * 30), self.options[i], (127, 127, 127))
    
class StartMenu(object):
    def __init__(self, prevMenu):
        self.prevMenu = prevMenu
        
    def handlekeys(self, keystate):
        return self
        
    def display(self):
        pass
class OptionsMenu(object):
    def __init__(self, prevMenu):
        self.prevMenu = prevMenu
    
    def handlekeys(self, keystate):
        return self
        
    def display(self):
        pass
class Quit(object):
    def __init__(self, prevMenu):
        self.prevMenu = prevMenu
    
    def handlekeys(self, keystate):
        return self
        
    def display(self):
        pass
