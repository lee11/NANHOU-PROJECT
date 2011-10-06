# Get a direction prefix letter based on the input direction component vectors.
# Use this to determine which Animation to get images from.
def getDirectionPrefix(x, y):
    if x == 0 and y == 0:
        return 'i'
    if y >= x:
        if y >= -x:
            return 'u'
        else:
            return 'l'
    else:
        if y >= -x:
            return 'r'
        else:
            return 'd'
