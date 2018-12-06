import sys
import random
import time

class Node():
    # root is black
    # leaves are black
    # red->children are black
    # number of black nodes to leaves is const
    def __init__(self, val, par, left = None, right = None, isRed = True, isNull = False):
        self.isRed = isRed
        self.left = left
        self.right = right
        self.val = val
        self.par = par
        self.isNull = isNull
        if not isNull:
            self.left = Node.createNullNode(self)
            self.right = Node.createNullNode(self)

    @staticmethod
    def createNullNode(par):
        return Node(0, par, isRed=False, isNull=True)

    # left < root <= right
    def insert(self, newVal):
        lastNode = None
        currNode = self
        # go all the way to the leaf
        while not currNode.isNull:
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
    
    def find(self, val):
        currNode = self
        while currNode is not None and currNode.val != val:
            if val < currNode.val:
                currNode = currNode.left
            elif val > currNode.val:
                currNode = currNode.right
        return currNode

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
        if not rightSonOldLeft.isNull:
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
        if not wasRoot:
            wasLeftSon = oldPar.left == self
            if wasLeftSon:
                oldPar.left = leftSon
            else:
                oldPar.right = leftSon
        if not leftSonOldRight.isNull:
            leftSonOldRight.par = self
        self.left = leftSonOldRight
        self.par = leftSon
        leftSon.par = oldPar
        if changeCol:
            self.isRed = False
            if not wasRoot:
                oldPar.isRed = True
    
    def rightRotateDel(self, changeCol):
        root = self
        parent = root.par
        root.par = parent.par
        if parent.par is not None:
            if parent.par.right ==  parent:
                parent.par.right = root
            else:
                parent.par.left = root
        right = root.right
        root.right = parent
        parent.par = root
        parent.left = right
        if right is not None:
            right.par = parent
        if changeCol:
            root.isRed = False
            parent.isRed = True
    
    def leftRotateDel(self, changeCol):
        root = self
        parent = root.par
        root.par = parent.par
        if parent.pare is not None:
            if parent.par.right == parent:
                parent.par.right = root
            else:
                parent.par.left = root
        left = root.left
        root.left = parent
        parent.par = root
        parent.right = left
        if left is not None:
            left.par = parent
        if changeCol:
            root.isRed = False
            parent.isRed = True
        
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
        if grand.left == self.par:
            return grand.right
        else:
            return grand.left
    
    def __str__(self):
        return str(self.val) + ("R" if self.isRed else "B")
    
    def print(self, level=0):
        print(f"{'__'*level}{self}")
        if not self.right.isNull:
            self.right.print(level+1)
            print()
        if not self.left.isNull:
            self.left.print(level+1)

    def remove(self, value, rbtree):
        currNode = self
        while not currNode.isNull and currNode.val != value:
            if value < currNode.val:
                currNode = currNode.left
            else:
                currNode = currNode.right
        if currNode.isNull:
            return 
        # go to far right if they're equal
        while not currNode.right.isNull and currNode.right == value:
            currNode = currNode.right
        # 1) convert to 0 or 1 child case
        if currNode.left.isNull or currNode.right.isNull:
            # since it has < 2 children
            currNode.remove01(rbtree)
            return
        succ = currNode.findSuccessor()
        succVal = succ.val
        succ.val = currNode.val
        currNode.val = succVal
        currNode.right.remove(value, rbtree)

    @staticmethod
    def switchNodes(par, child, rbtree):
        # switch child and parent, and parent gets lost in the process
        child.par = par.par
        if par.par is None:
            rbtree.root = child
        else:
            isLeft = par.par.left == par
            if isLeft:
                par.par.left = child
            else:
                par.par.right = child

    # remove this node with 0 or 1 children
    def remove01(self, rbtree):
        child = self.left if not self.left.isNull else self.right
        Node.switchNodes(self, child, rbtree)        

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
        if not Node.isBlack(sib):
            if self.par.left == sib: 
                sib.rightRotateDel(True)
            else:
                sib.leftRotateDel(True)
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
                sib.left.rightRotateDel(True)
            elif not isLeftChild and Node.isBlack(sib.left) and Node.isBlack(sib.right) == False:
                sib.right.leftRotateDel(True)
        self.del_case6(rbtree)
        
    def del_case6(self, rbtree):
        sib = self.sibling()
        sib.isRed = sib.par.isRed
        sib.par.isRed = False
        if self == self.par.left:
            sib.right.isRed = False
            sib.leftRotateDel(False)
        else:
            sib.left.isRed = False
            sib.rightRotateDel(False)
        if sib.isRoot(): 
            rbtree.root = sib

    # finds a successor in right subtree
    def findSuccessor(self):
        curr = self.right
        while not curr.left.isNull:
            curr = curr.left
        # go to far right if they're equal
        while not curr.right.isNull and curr.right.val == curr.val:
            curr = curr.right
        return curr
    
    def toSortedList(self):
        ret = []
        if not self.left.isNull:
            ret = self.left.toSortedList()
        ret.append(self.val)
        if not self.right.isNull:
            ret.extend(self.right.toSortedList())
        return ret

# RBTree is a wrapper around Nodes, which actually do all the work
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
    
    def toSortedList(self):
        if self.root is None:
            return []
        return self.root.toSortedList()

    def print(self, level=0):
        if self.root is None:
            print("Empty tree.")
            return
        self.root.print()
    
    def find(self, val):
        if self.root is None:
            return None
        return self.root.find(val)

def test():
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
    tree.insert(4)
    tree.remove(99)
    tree.insert(10)
    tree.insert(55)
    tree.insert(15)
    tree.insert(-3)
    tree.insert(777)
    tree.print()
    print("finding...", tree.find(44))

    print("sorted = ", tree.toSortedList())
    print("Bye")

def main():
    if len(sys.argv) == 1:
        n = 30000
        #test()
        #return
    else:
        n = int(sys.argv[1])
        print(n)
    for n in range(1000_000, 1000_001, 100_000):#range(500000, 1000_000, 100_000):
        start = time.time()

        tree = RBTree()
        for _ in range(0,n):
            x = random.randint(-1000_000, 1000_000)
            tree.insert(x)

        end = time.time()
        timeLength =  end - start
        print(n, timeLength)


if __name__ == "__main__":
    main()