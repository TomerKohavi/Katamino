import shape

def convertToShapes(arr):
    for quest in arr:
        for x in xrange(len(quest)):
            quest[x] = shape.shapes[quest[x]]

def getSlamQuestion(questNum, penta):
    if questNum<0 or questNum>=len(slamQuestions) or penta<3 or penta>9:
        return None
    return slamQuestions[questNum][:penta]

def getLittleSlamQuestion(questNum, penta):
    if questNum<0 or questNum>=len(littleSlamQuestions) or penta<3 or penta>9:
        return None
    return littleSlamQuestions[questNum][:penta]

def getDefaultQuestion():
    default = [1,2,3,4,5,6,7,8,9,10,11,12]
    for x in xrange(len(default)):
        default[x] = shape.shapes[default[x]]
    return default


littleSlamQuestions = []

littleSlamQuestions.append([2,3,10,6,11,8,5,4,9])

littleSlamQuestions.append([4,6,7,2,8,3,10,11,5])

littleSlamQuestions.append([2,5,6,3,4,7,8,9,10])

littleSlamQuestions.append([3,6,7,4,5,9,11,10,2])

littleSlamQuestions.append([2,4,5,8,7,10,9,3,11])

littleSlamQuestions.append([6,7,9,3,10,4,2,11,8])

littleSlamQuestions.append([2,5,6,8,3,11,4,9,7])

slamQuestions = []

slamQuestions.append([2,3,5,7,8,9,4,11,10])

slamQuestions.append([2,4,6,10,11,8,3,5,7])

slamQuestions.append([3,6,7,9,10,11,5,2,8])

slamQuestions.append([2,3,4,6,11,10,9,8,5])

slamQuestions.append([2,5,6,9,11,3,7,10,4])

slamQuestions.append([2,6,7,8,10,9,4,3,11])

slamQuestions.append([3,5,6,8,11,2,7,4,9])

slamQuestions.append([2,3,5,10,11,8,6,7,4])

slamQuestions.append([2,3,5,6,9,7,8,11,10])

slamQuestions.append([4,5,6,7,9,11,2,10,3])

slamQuestions.append([2,3,6,8,11,4,10,9,7])

slamQuestions.append([2,6,7,9,11,3,8,4,5])

slamQuestions.append([3,4,5,6,7,2,10,9,8])

slamQuestions.append([2,5,6,7,11,4,10,3,9])

convertToShapes(littleSlamQuestions)
convertToShapes(slamQuestions)