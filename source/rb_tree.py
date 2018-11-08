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
                z.leftRotate(False)
            # (case 3 goes after 2 ) z = z.parent
            # case 3: z.uncle = black(line) =>  rotate z.grandparent opposite of z and recolor
            # anyhow, now that triangle is gone, they are in a line. rotate grandparent
            z.par.isRed = False
            grampa = z.grandparent()
            grampa.isRed = True
            grampa.rightRotate(False)
            z.insert_repair()
        # same as the last block, but mirrored
        else:
            isTriangle = self.par.left == self
            z = self
            if isTriangle:
                z = self.par
                z.rightRotate(False)
            z.par.isRed = False
            grampa = z.grandparent()
            grampa.isRed = True
            grampa.leftRotate(False)
            z.insert_repair()

    # become left child of right son
    def leftRotate(self, changeCol):
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
        if changeCol:
            self.isRed = False
            oldPar.isRed = True

    # become right child of left son
    def rightRotate(self, changeCol):
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
        if changeCol:
            self.isRed = False
            oldPar.isRed = True

    def parent(self):
        return self.par

    def sibling(self):
        if self.par is None:
            return None
        if self.par.left == self:
            return self.par.right
        else:
            return self.par.left
    
    @staticmethod
    def isBlack(self):
        if self is None:
            return True
        return not self.isRed
    
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

    def remove(self, value, rbtree):
        # TODO NAVIGATE. not sure what to do with duplicates removal
        currNode = self
        while currNode and currNode.val != value:
            if value < currNode.val:
                currNode = currNode.left
            else:
                currNode = currNode.right
        if currNode is None:
            return 
        # go to far right if they're equal
        while currNode.right and currNode.right == value:
            currNode = currNode.right
        # 1) convert to 0 or 1 child case
        if self.left is None or self.right is None:
            # since it has < 2 children
            self.remove01(rbtree)
        succ = self.findSuccessor()
        succVal = succ.val
        succ.val = self.val
        self.val = succVal
        self.right = self.right.remove(value, rbtree)

    @staticmethod
    def replaceNode(par, child, rbtree):
        # switch child and parent, and parent gets lost in the process
        if par.par:
            isLeft = par.par.left == par
            if isLeft:
                par.par.left = child
            else:
                par.par.right = child
        else:
            rbtree.root = child

    # remove this node with 0 or 1 children
    def remove01(self, rbtree):
        assert not self.right or not self.left, "at least 1 should be None"
        child = self.left if self.left else self.right
        Node.replaceNode(self, child, rbtree)        

        if Node.isBlack(self):
            if Node.isBlack(child) == False:
                child.isRed = False
            else:
                # 3) not red node and no red children: 6 "double-black" cases.
                # Element is deleted now, but fixes are done with these cases
                child.del_case1(rbtree)

    # https://www.youtube.com/watch?v=CTvfzU_uNKE
    # source of 6 double-black cases

    # root case
    def del_case1(self, rbtree):
        if self.isRoot():
            rbtree.root = self
        self.del_case2(rbtree)
    
    def del_case2(self, rbtree):
        sib = self.sibling()
        assert sib is not None, "Sib is None - what would rotation even mean then? It shouldn't happen"
        if not Node.isBlack(sib):
            if self.par.left == sib: 
                sib.rightRotate(True)
            else:
                sib.leftRotate(True)
            if sib.isRoot():
                rbtree.root = sib
        self.del_case3(rbtree)

    
    def del_case3(self, rbtree):
        sib = self.sibling()
        if Node.isBlack(self.par) and Node.isBlack(sib) and Node.isBlack(sib.left) and Node.isBlack(sib.right):
            sib.isRed = True
            self.par.del_case1(rbtree)
        else:
            self.del_case4(rbtree)


    def del_case4(self, rbtree):
        sib = self.sibling()
        if Node.isBlack(sib.par) == False and Node.isBlack(sib) and Node.isBlack(sib.left) and Node.isBlack(sib.right):
            sib.isRed = True
            self.par.isRed = False
        else:
            self.del_case5(rbtree)
        
    def del_case5(self, rbtree):
        sib = self.sibling()
        if Node.isBlack(sib):
            isLeftChild = self.par.left == self
            if isLeftChild and Node.isBlack(sib.right) and Node.isBlack(sib.left) == False:
                sib.left.rightRotate(True)
            elif not isLeftChild and Node.isBlack(sib.left) and Node.isBlack(sib.right) == False:
                sib.right.left(True)
        self.del_case6(rbtree)
        
    def del_case6(self, rbtree):
        sib = self.sibling()
        sib.isRed = sib.par.isRed
        sib.par.isRed = False
        if self == self.par.left:
            sib.right.isRed = False
            sib.leftRotate(False)
        else:
            sib.elft.isRed = False
            sib.rightRotate(False)
        if sib.isRoot():
            rbtree.root = sib

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
        self.root.remove(newVal, self)
        
    def print(self, level=0):
        if self.root is None:
            print("Empty tree.")
            return
        self.root.print()
        
def main():
    print("Hi")
    tree = RBTree()
    

    tree.insert(3)
    tree.insert(4)
    tree.insert(5)
    tree.insert(1)
    tree.insert(2)

    tree.print()
    print("----REMOVING------")
    tree.remove(4)
    tree.print()
    print("Bye")

if __name__ == "__main__":
    main()