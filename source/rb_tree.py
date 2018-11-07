class Node():
    def __init__(self, val, par, left = None, right = None, isRed = True):
        self.isRed = isRed
        self.left = left
        self.right = right
        self.val = val
        self.par = par

    # left < root <= right
    def insert(self, newVal):
        lastNode = None
        currNode = self
        if newVal == self.val:
            assert "TODO: decide whether to ignore or not"
        # go all the way to the leaf
        while currNode is not None:
            lastNode = currNode
            if newVal < self.val:
                currNode = self.left
            else:
                currNode = self.right
        newNode = Node(newVal, par=lastNode)
        if newVal < lastNode:
            lastNode.left = newNode
        else:
            lastNode.right = newNode
        
        newNode.insert_repair()
        return newNode.find_root()
        
    def find_root(self):
        curr = self
        while curr.par is not None:
            curr = curr.par
        return curr

    # called after inserting a new node,
    # and sometimes recursively
    def insert_repair(self):
        if self.par is None:
            self.isRed = False
            return
        if not self.par.isRed:
            # his parent is black, do nothing
            return
        # since his parent is red, repair is needed
        uncle = self.uncle()
        isUncleRed = False if uncle is None else uncle.isRed
        if isUncleRed:
            # case 1: z.uncle = red => recelor parent, grandp, uncle
            return

        # else, uncle is black
        # case 2: z.uncle = black(triangle) => rotate z.parent to opposite of z
        # case 3: z.uncle = black(line) =>  rotate z.grandparent opposite of z and recolor
        
    def remove(self, value):
        pass
    
    def case1(self):
        pass
    
    def case2(self):
        pass
    
    def case3(self):
        pass
# root is black
# leaves are black
# red->children are black
# number of black nodes to leaves is const

# at fisrt, z is red

# if parent is black then chill

# case 0: z is root => z is black
# case 1: z.uncle = red => recelor parent, grandp, uncle
# case 2: z.uncle = black(triangle) => rotate z.parent to opposite of z
# case 3: z.uncle = black(line) =>  rotate z.grandparent opposite of z and recolor
    def leftRotate(self):
        pass
    
    def rightRotate(self):
        pass

    def parent(self):
        return self.par
    
    def isRoot(self):
        return self.par is None

    def grandparent(self):
        if self.par is None:
            return None
        return self.par.par
    
    def uncle(self):
        grand = self.grandparent()
        if grand is None:
            assert "TODO: Maybe this shouldn't happen"
            return None
        if grand.left == self.par:
            return grand.right
        else:
            return grand.left
    
    def __str__(self):
        return str(self.val) + "R" if self.isRed else "B"
    
    def __print(self, level=0):
        print(f"{'__'*level}{self}")
        if self.right is not None:
            self.right.__print(level+1)
        if self.left is not None:
            self.left.__print(level+1)
        

class RBTree():
    def __init__(self, root=None):
        self.root = None
    def insert(self, newVal):
        if self.root is None:
            self.root = Node(newVal, par=None, isRed=False)
        else:
            self.root = self.root.insert(newVal)

    def remove(self, newVal):
        self.root = self.root.remove(newVal)
        
    def printTree(self, level=0):
        if self.root is None:
            print("Empty tree.")
            return
        self.root.__print()
        
        
        


def main():
    print("Begin")

if __name__ == "__main__":
    main()