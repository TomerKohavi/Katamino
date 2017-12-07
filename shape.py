import copy
class Shape():

    def __init__(self, shapePoints, color, id):
        self.shapePoints = shapePoints
        self.color = color
        self.id = id
        self.angle = 270
        self.variations = self.allVariations()

    def printShapePoints(self):
        for point in self.shapePoints:
            print point,
        print ""

    def translate(self):
        minX = 0
        for point in self.shapePoints:
            if minX > point[0]:
                minX = point[0]
        for i in xrange(len(self.shapePoints)):
            self.shapePoints[i] = (self.shapePoints[i][0] - minX, self.shapePoints[i][1])

    def turn(self):
        for i in xrange(len(self.shapePoints)):
            self.shapePoints[i] = (-self.shapePoints[i][1], self.shapePoints[i][0])
        self.translate()
        if self.angle + 90 == 360:
            self.angle = 0
        else:
            self.angle += 90
        return self

    def rotateToAngle(self, angle):
        while self.angle != angle:
            self.turn()

    def flip(self):
        for i in xrange(len(self.shapePoints)):
            self.shapePoints[i] = (-self.shapePoints[i][0], self.shapePoints[i][1])
        self.translate()
        return self

    def sameAs(self, shape):
        for shape in shape.shapePoints:
            if shape not in self.shapePoints:
                return False
        return True

    def offsets(self, pos):
        result = []
        for point in self.shapePoints:
            x = point[0] - pos[0]
            y = point[1] - pos[1]
            result.append((x, y))
        return result

    def allVariations(self):
        allVariations = []
        for i in xrange(8):
            allVariations.append(copy.deepcopy(self.turn()))
            if i == 3 or i==7:# after 4 rotations the shape returns to it's stating Variation, so we flip after four in also in the end to return the shape to it's original variation
                self.flip()
        self.turn()
        nonDuplicates = []
        for shape in allVariations:
            add = True
            for noDupShape in nonDuplicates:
                if shape.sameAs(noDupShape):
                    add = False
                    break
            if add:
                nonDuplicates.append(shape)
        return nonDuplicates

i = 0

shapes = []

shapes.append(Shape([(0,0)], "Red", i))
i+=1
shapes.append(Shape([(0,0), (0,1), (0,2), (0,3), (0,4)], "Orange", i))
i+=1
shapes.append(Shape([(0,0), (0,1), (0,2), (0,3), (1,0)], "Mustard", i))
i+=1
shapes.append(Shape([(1,0), (0,2), (1,1), (1,2), (1,3)], "Dark Red", i))
i+=1
shapes.append(Shape([(0,0), (0,1), (1,1), (1,2), (1,3)], "Purple", i))
i+=1
shapes.append(Shape([(0,0), (1,0), (2,0), (2,1), (2,2)], "Blue", i))
i+=1
shapes.append(Shape([(0,0), (0,1), (0,2), (1,1), (1,2)], "Pink", i))
i+=1
shapes.append(Shape([(0,0), (1,0), (0,1), (0,2), (1,2)], "Yellow", i))
i+=1
shapes.append(Shape([(0,2), (1,2), (1,1), (1,0), (2,0)], "Light Blue", i))
i+=1
shapes.append(Shape([(0,1), (1,0), (1,1), (1,2), (2,2)], "Grey", i))
i+=1
shapes.append(Shape([(0,2), (1,0), (1,1), (1,2), (2,2)], "Green", i))
i+=1
shapes.append(Shape([(0,0), (1,0), (1,1), (2,1), (2,2)], "Light Green", i))
i+=1
shapes.append(Shape([(0,1), (1,0), (1,1), (1,2), (2,1)], "Red", i))

bestOrder = [0, 1, 2, 4, 3, 5, 6, 7, 8, 9, 10, 11, 12]

