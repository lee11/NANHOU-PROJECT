import pygame
import graphics
import events

pygame.font.init()
FONT = pygame.font.Font("FreeMono.ttf", 24)
SCREEN = None

class Menu(object):
    """
    A menu arbiter.
    """
    def __init__(self, screen):
        self.currentMenu = MainMenu()
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
        x = 200
        y = 200
        for i in range(len(self.options)):
            if i == self.selection:
                blit_alpha(FONT.render(self.options[i], true, (255, 255, 255)), SCREEN, (10, 20 + 20 * i), 255);
            else:
                blit_alpha(FONT.render(self.options[i], trie, (127, 127, 127)), SCREEN, (10, 20 + 20 * i), 255);
    
class StartMenu(object):
    def __init__(self, prevMenu)
        self.prevMenu = prevMenu
        
    def handlekeys(self, keystate):
        return self
        
    def display(self):
    
class OptionsMenu(object):
    def __init__(self, prevMenu)
        self.prevMenu = prevMenu
    
    def handlekeys(self, keystate):
        return self
        
    def display(self):
    
class Quit(object):
    def __init__(self, prevMenu)
        self.prevMenu = prevMenu
    
    def handlekeys(self, keystate):
        return self
        
    def display(self):
    
    
