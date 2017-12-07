import cPickle
import timeit

boardHeight = 5
tries = 1

pickle_in = open("learning.pickle", "rb")
learn = cPickle.load(pickle_in)

class Ai:

    def bestOrder(self):
        bestOrder = learn.bestOrder
        arr = []
        for i in bestOrder:
            for shape in self.shapes:
                if shape.id == i:
                    arr.append(shape)
        self.shapes = arr

    def __init__(self, question):
        self.shapes = question
        self.bestOrder()
        self.numOfShapes = len(self.shapes)
        self.board = [[0 for i in xrange(self.numOfShapes)] for j in xrange(boardHeight)]

    def changeQuest(self, question):
        if question:
            self.shapes = question
            self.numOfShapes = len(self.shapes)
            self.board = [[0 for i in xrange(self.numOfShapes)] for j in xrange(boardHeight)]

    def clearBoard(self):
        self.board = [[0 for i in xrange(self.numOfShapes)] for j in xrange(boardHeight)]

    def shapeFits(self, offset, shape):
        for point in shape.shapePoints:
            newPoint = (point[0] - offset[0], point[1] - offset[1])
            if newPoint[0] < 0 or newPoint[0] >= boardHeight or newPoint[1] < 0 or newPoint[1] >= self.numOfShapes or self.board[newPoint[0]][newPoint[1]] != 0:
                return False
        return True

    def addShape(self, offset, shape):
        for point in shape.shapePoints:
            newPoint = (point[0] - offset[0], point[1] - offset[1])
            self.board[newPoint[0]][newPoint[1]] = shape.id

    def removeShape(self, shape):
        for i in xrange(boardHeight):
            for j in xrange(self.numOfShapes):
                if self.board[i][j] == shape.id:
                    self.board[i][j] = 0

    def solved(self):
        for row in self.board:
            for num in row:
                if num == 0:
                    return False
        return True

    def groupSize(self, board, i, j):
        if i<0 or i >= len(board) or j<0 or j >= len(board[0]) or not board[i][j]:
            return 0
        board[i][j] = False
        if self.board[i][j]!=0:
            return 0
        return 1+self.groupSize(board, i+1, j)+self.groupSize(board, i, j+1)+self.groupSize(board, i-1, j)+self.groupSize(board, i, j-1)

    def possible(self):
        board = [[True for i in xrange(self.numOfShapes)] for j in xrange(boardHeight)]
        for i in xrange(len(board)):
            for j in xrange(len(board[0])):
                if self.board[i][j] == 0 and board[i][j]:
                    if self.groupSize(board, i, j) % 5 != 0:
                        return False
        return True

    def availableSpot(self):
        for j in xrange(self.numOfShapes):
            for i in xrange(boardHeight):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def solve(self, shapes):
        global tries
        pos = self.availableSpot()
        if not pos:
            return True
        for x,shape in enumerate(shapes):
            for shapeVar in shape.variations:
                for offset in shapeVar.offsets(pos):
                    if self.shapeFits(offset, shapeVar):
                        self.addShape(offset, shapeVar)
                        if not self.possible():
                            self.removeShape(shapeVar)
                        else:
                            copyList = shapes[:]
                            copyList.pop(x)
                            if len(copyList) != 0:
                                if self.solve(copyList):
                                    return True
                                self.removeShape(shapeVar)
                            else:
                                return True
        tries += 1
        return False

    def shapesOrder(self):
        shapesOrder = []
        for j in xrange(self.numOfShapes):
            for i in xrange(boardHeight):
                if shapesOrder.count(self.board[i][j]) == 0:
                    shapesOrder.append(self.board[i][j])
        return shapesOrder

    def printBoard(self):
        for row in self.board:
            for num in row:
                print repr(num).rjust(2),
            print ""
        print ""
