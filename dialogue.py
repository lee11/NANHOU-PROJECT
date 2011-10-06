import animation
import os

TEXTLIMIT = 60

class Dialogue(object):
    
    def __init__(self, prefixL, prefixR, text, textDirStr = '.', prfDirStr = '.'):
        pathToText = os.path.join(textDirStr, text)
        f = open(pathToText, 'r')
        self.retlist = []   #contains all tuples of dialogue
        self.index = -1
        self.Limg = animation.loadImages(prefixL, dirStr = prfDirStr)
        self.Rimg = animation.loadImages(prefixR, dirStr = prfDirStr)
        for line in f:
            words = line.split()
            tempL = int(words[0])
            if tempL == -1:
                tempRefL = None
            else:
                tempRefL = self.Limg[tempL]
            tempR = int(words[1])
            if tempR == -1:
                tempRefR = None
            else:
                tempRefR = self.Rimg[tempR]
            tempF = words[2]
            statements = []
	    count = 0
            index = 0
            # Find the start of the text string within the line
            for c in line:
                if count == 3:
                    break
                else:
                    index += 1
                    if c == ' ':
                        count += 1
            start = index
            count = 0
            lastspace = None
            linelen = len(line) - 1
            # While going through the chars, mark the last space
            # visited while keeping track of the number of chars
            # visited. If the limit is reached or the end of the
            # string is reached, append a new substring to the
            # statements list.
            for c in range(index, len(line)):
                if count > TEXTLIMIT:
                    statements.append(line[start:lastspace])
                    count = 0
                    start = lastspace + 1
                elif c == linelen:
                    statements.append(line[start:-1])
                else:
                    count += 1
                    if line[c] == ' ':
                        lastspace = c
            for s in statements:
                self.retlist.append((tempRefL, tempRefR, tempF, s))
        self.retlen = len(self.retlist) - 1
	f.close()
        
    def get(self):
        if self.index >= self.retlen:
            return None
        else:
            self.index += 1
            return self.retlist[self.index]
