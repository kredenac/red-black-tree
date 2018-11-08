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
        # go all the way to the leaf
        while currNode is not None:
            lastNode = currNode
            if newVal < currNode.val:
                currNode = currNode.left
            else:
                currNode = currNode.right

        newNode = Node(newVal, par=lastNode)
        if newVal < lastNode.val:
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
    # and recursively
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
            # case 1: z.uncle = red => recolor parent, grandp, uncle
            grampa = self.grandparent()
            self.par.isRed = False
            grampa.isRed = True
            uncle.isRed = False
            grampa.insert_repair()
            return

        # else, uncle is black

        isParLeftOfGramp = self.par.par.left == self.par
        if isParLeftOfGramp:
            # triangle is when z, parent and grandparent are not in a straight line
            isTriangle = self.par.right == self
            z = self
            # case 2: z.uncle = black(triangle) => rotate z.parent to opposite of z 
            if isTriangle:
                z = self.par
                z.leftRotate()
            # (case 3 goes after 2 ) z = z.parent
            # case 3: z.uncle = black(line) =>  rotate z.grandparent opposite of z and recolor
            # anyhow, now that triangle is gone, they are in a line. rotate grandparent
            z.par.isRed = False
            grampa = z.grandparent()
            grampa.isRed = True
            grampa.rightRotate()
            z.insert_repair()
        # same as the last block, but mirrored
        else:
            isTriangle = self.par.left == self
            z = self
            if isTriangle:
                z = self.par
                z.rightRotate()
            z.par.isRed = False
            grampa = z.grandparent()
            grampa.isRed = True
            grampa.leftRotate()
            z.insert_repair()

    # become left child of right son
    def leftRotate(self):
        oldPar = self.par
        wasRoot = self.isRoot()
        rightSon = self.right
        rightSonOldLeft = rightSon.left
        rightSon.left = self
        if not wasRoot:
            wasLeftSon = oldPar.left == self
            if wasLeftSon:
                oldPar.left = rightSon
            else:
                oldPar.right = rightSon
        if rightSonOldLeft is not None:
            rightSonOldLeft.par = self
        self.right = rightSonOldLeft
        self.par = rightSon
        rightSon.par = oldPar
    
    # become right child of left son
    def rightRotate(self):
        oldPar = self.par
        wasRoot = self.isRoot()
        leftSon = self.left
        leftSonOldRight = leftSon.right
        leftSon.right = self
        wasLeftSon = oldPar.left == self
        if not wasRoot:
            if wasLeftSon:
                oldPar.left = leftSon
            else:
                oldPar.right = leftSon
        if leftSonOldRight is not None:
            leftSonOldRight.par = self
        self.left = leftSonOldRight
        self.par = leftSon
        leftSon.par = oldPar

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
        return str(self.val) + ("R" if self.isRed else "B")
    
    def print(self, level=0):
        print(f"{'__'*level}{self}")
        if self.right is not None:
            self.right.print(level+1)
            print()
        if self.left is not None:
            self.left.print(level+1)

    def remove(self, value):
        # TODO NAVIGATE. not sure what to do with duplicates removal
        currNode = self
        while currNode and currNode.val != value:
            if value < currNode.val:
                currNode = currNode.left
            else:
                currNode = currNode.right
        if currNode is None:
            return self
        # go to far right if they're equal
        while currNode.right and currNode.right == value:
            currNode = currNode.right
        # 1) convert to 0 or 1 child case
        succ = self.findSuccessor()
        if succ is None:
            # since it has < 2 children
            return self.remove01(value)
        succVal = succ.val
        succ.val = self.val
        self.val = succVal
        self.right = succ.right.remove01(value)
        return self

    # remove a node with 0 or 1 children
    def remove01(self, value):
        assert not self.right or not self.left, "at least 1 should be None"
        # B if node is red find a successor, swap and delete.

        # 2) if node to be deleted is red, or child is red
        #       then do replace 
        if self.isRed:
            par = self.par
            if not self.left and not self.right:
                # if no children, delete itself
                if par is None:
                    return None
                # set to where parent pointed to self to none
                par.left = par.left if par.left != self else None
                par.right = par.right if par.right != self else None

            assert par is not None, "Parent should never be none here"
            thatOneChild = self.left if self.left else self.right
            thatOneChild.par = par
            return thatOneChild

        # 3) double black node: 6 cases...
        pass

    # finds a successor in right subtree
    def findSuccessor(self):
        assert self.right is not None, "right child is None in findSuccessor"
        curr = self.right
        while curr.left:
            curr = curr.left
        # go to far right if they're equal
        while curr.right and curr.right.val == curr.val:
            curr = curr.right
        return curr

# root is black
# leaves are black
# red->children are black
# number of black nodes to leaves is const
class RBTree():
    def __init__(self, root=None):
        self.root = root
    def insert(self, newVal):
        if self.root is None:
            self.root = Node(newVal, par=None, isRed=False)
        else:
            self.root = self.root.insert(newVal)

    def remove(self, newVal):
        self.root = self.root.remove(newVal)
        
    def print(self, level=0):
        if self.root is None:
            print("Empty tree.")
            return
        self.root.print()
        
def main():
    print("Hi")
    tree = RBTree()
    
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.insert(5)
    tree.insert(1)
    tree.insert(1)


    tree.print()

    print("Bye")

if __name__ == "__main__":
    main()