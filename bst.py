def biggerThan(list1, list2):
    for i in xrange(len(list1)):
        if list1[i] and not list2[i]:
            return True
        elif not list1[i] and list2[i]:
            return False
    return False

def isSame(list1, list2):
    for i in xrange(len(list1)):
        if list1[i] != list2[i]:
            return False
    return True


class Node:
    def __init__(self, val):
        self.val = val
        self.leftChild = None
        self.rightChild = None

    def getChildren(self):
        children = []
        if (self.leftChild != None):
            children.append(self.leftChild)
        if (self.rightChild != None):
            children.append(self.rightChild)
        return children


class BST:
    def __init__(self):
        self.root = None

    def setRoot(self, val):
        self.root = Node(val)

    def insert(self, val):
        if (self.root is None):
            self.setRoot(val)
            return True
        else:
            return self.insertNode(self.root, val)

    def insertNode(self, currentNode, val):
        if isSame(val, currentNode.val):
            return False
        elif (biggerThan(val, currentNode.val)):
            if (currentNode.leftChild):
                self.insertNode(currentNode.leftChild, val)
            else:
                currentNode.leftChild = Node(val)
                return True
        else:
            if (currentNode.rightChild):
                self.insertNode(currentNode.rightChild, val)
            else:
                currentNode.rightChild = Node(val)
                return True

    def find(self, val):
        return self.findNode(self.root, val)

    def findNode(self, currentNode, val):
        if (currentNode is None):
            return False
        elif (isSame(val, currentNode.val)):
            return True
        elif (biggerThan(val, currentNode.val)):
            return self.findNode(currentNode.leftChild, val)
        else:
            return self.findNode(currentNode.rightChild, val)