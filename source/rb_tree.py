class node(object):
    def __init__(self, val, par, left = None, right = None, isBlack = False):
        self.isBlack = isBlack
        self.left = left
        self.right = right
        self.val = val
        self.par = par

    def insert(self, newVal):
        pass
    
    def remove(self, value):
        pass
    
    def leftRotate(self):
        pass
    
    def rightRotate(self):
        pass

    def parent(self):
        pass
    
    def grandparent(self):
        pass
    
    def uncle(self):
        pass

    def rotateLeft(self):
        pass
    
    def rotateRight(self):
        pass
# root is black
# leaves are black
# red->children are black
# number of black nodes to leaves is const

# case 0: z is root => z is black
# case 1: z.uncle = red => recelor parent, grandp, uncle
# case 2: z.uncle = black(triangle) => rotate z.parent to opposite of z
# case 3: z.uncle = black(line) =>  rotate z.grandparent opposite of z

def main():
    print("Begin")

if __name__ == "__main__":
    main()