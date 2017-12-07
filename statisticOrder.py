import cPickle
import shape
from bst import BST

numOfShapes = len(shape.shapes)

def binary(order):
    bin = [False for i in xrange(numOfShapes)]
    for shape in order:
        bin[shape] = True
    return bin


class Learning:

    def __init__(self):
        self.questions = BST()
        self.sumOfOrders = [0 for i in xrange(numOfShapes)]
        self.numOfAppearance = [0 for i in xrange(numOfShapes)]
        self.bestOrder = [i for i in xrange(numOfShapes)]

    def add(self, order):
        if not self.questions.find(binary(order)): # if question doesn't already exist
            self.questions.insert(binary(order))
            for x, shape in enumerate(order):
                self.sumOfOrders[shape] += x
                self.numOfAppearance[shape] += 1
        else:
            print "Already Been Added"

    def updateOrder(self):

        sumOfOrders = [-1 for i in xrange(numOfShapes)]
        max = 0
        for i in xrange(numOfShapes):
            if self.numOfAppearance[i] != 0:
                sumOfOrders[i] = (self.sumOfOrders[i]/self.numOfAppearance[i])
                if max < sumOfOrders[i]:
                    max = sumOfOrders[i]

        for i in xrange(numOfShapes):
            if sumOfOrders[i] == -1:
                sumOfOrders[i] = max+1

        bestOrder = []

        for i in xrange(len(sumOfOrders)):
            for j in xrange(len(sumOfOrders)):
                if bestOrder.count(j) == 0:
                    min = j
                    break

            for j in xrange(len(sumOfOrders)):
                if sumOfOrders[j] != -1 and sumOfOrders[j] < sumOfOrders[min]:
                    min = j
            sumOfOrders[min] = -1
            bestOrder.append(min)

        self.bestOrder = bestOrder