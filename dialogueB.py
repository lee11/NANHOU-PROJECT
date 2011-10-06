import animation, os

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
                tempRefR = self.Limg[tempR]
            tempF = words[2]
            statements = []
            wLen = len(words) - 1
            line = ''
            for x in range(3, len(words)):
                if len(line) > TEXTLIMIT:
                    statements.append(line[0:-1])
                    line = line[-1:]
                    line += words[x] + ' '
                    if x == wLen:
                        print('line finished. statement stored.')
                        statements.append(line[0:-1])
                    continue
                else:
                    line += words[x] + ' '
                    if x == wLen:
                        print('line finished. statement stored.')
                        statements.append(line[0:-1])
                  
            for s in statements:
		print s
                self.retlist.append((tempRefL, tempRefR, tempF, s))

        self.retlen = len(self.retlist) - 1
	f.close()
        
    def get(self):
        if self.index >= self.retlen:
            return None
        else:
            self.index += 1
            return self.retlist[self.index]
