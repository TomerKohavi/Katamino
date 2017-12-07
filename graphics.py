import copy
import questions
import ai
import timeit
import shape
import math
import cPickle
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics import Rotate
from kivy.graphics.context_instructions import PopMatrix, PushMatrix
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from win32api import GetSystemMetrics

from kivy.config import Config
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')

DEFAULT_WIDTH = 2560
DEFAULT_HEIGHT = 1440

WIDTH = GetSystemMetrics(0)
HEIGHT = WIDTH * float(9)/16
Window.size = (WIDTH, HEIGHT)
Ratio = ((float(4)/3) * float(WIDTH)/DEFAULT_WIDTH, ((float(4)/3) * float(HEIGHT)/DEFAULT_HEIGHT))
Window.fullscreen = 'auto'

SQUARE = 82.3 * Ratio[0]

FileLoc = "C:\Users\Tomer\PycharmProjects\SchoolProject/"

pickle_in = open("learning.pickle", "rb")
learn = cPickle.load(pickle_in)


class Graphics(Image):
    def __init__(self):
        super(Graphics, self).__init__()
        self.source = FileLoc + 'Tomer KATAMINO\playscreen2.png'
        self.pc = ai.Ai(questions.getDefaultQuestion()) #default question
        self.placed = []
        self.currentShape = None
        self.questmode = False
        self.allShapes = []
        self.showShapes()
        self.buffer = Buffer(12)
        self.clearButton = ClearButton()
        self.solveButton = SolveButton()
        self.questSelect = QuestionSelect()
        self.questButton = QuestionButton('Questions')
        self.returnButton = QuestionButton('Return')
        self.pickButton = QuestionButton('Pick', (100, 750))
        self.wonButton = WonButton()
        self.add_widget(self.questButton)
        self.add_widget(self.clearButton)
        self.add_widget(self.solveButton)
        self.add_widget(self.buffer)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, *args):
        if self.questmode:
            return
        key = args[1][1]
        if self.currentShape == None:
            return
        if key == 'numpad0' or key == '0':
            self.currentShape.rotate()
        elif key == 'numpad1' or key == '1':
            self.currentShape.flip()
        elif key == 'enter':
            self.currentShape.place()
        else:
            self.currentShape.move(key) #if it's not up, down, right or left the func won't do anything

    def showShapes(self):
        lastPos = -95 * Ratio[0]
        for i in xrange(12):
            if i+1 == 2:
                lastPos += 95 * Ratio[0]
            elif i+1<8 and i+1 != 6:
                lastPos += 130 * Ratio[0]
            else:
                lastPos += 170 * Ratio[0]
            shape = shapeButton((lastPos, 100 * Ratio[1]), i + 1)
            self.allShapes.append(shape)
            self.add_widget(shape)

    def clear(self):
        for shape in self.placed:
            self.remove_widget(shape)
            self.allShapes[shape.shapeid-1].opacity = 1
        self.pc.clearBoard()
        self.placed = []

    def addQuestion(self, (i,j)):
        self.pc.changeQuest(questions.getLittleSlamQuestion(i,j+1))
        self.buffer.move(j+1)
        self.clear()
        for shape in self.allShapes:
            shape.opacity = 0
        for shape in self.pc.shapes:
            self.allShapes[shape.id-1].opacity = 1
        self.board = [[0 for i in xrange(len(self.pc.shapes))] for j in xrange(5)]

    def pits(self, shapeImg): # if shape fits in board place it and return True, otherwise return false0
        myShape = copy.deepcopy(shape.shapes[shapeImg.shapeid])
        if shapeImg.flipped:
            myShape.rotateToAngle(270)
            myShape.flip()
        myShape.rotateToAngle(shapeImg.rot.angle)
        offset = shapeImg.getArrayPos()
        if self.pc.shapeFits(offset, myShape):
            self.pc.addShape(offset, myShape)
            return True
        return False

    # def visualSolution(self):
    #     for row in self.pc.board:
    #         for num in row:
    #             if


class shapeButton(ButtonBehavior, Image):
    def __init__(self, (x,y), id):
        self.shapeid = id
        super(shapeButton, self).__init__()
        self.source = FileLoc + 'Tomer KATAMINO\_' + str(self.shapeid) + '.png'
        self.pos = (x,y)
        self.size = (self.width * 1.5 * Ratio[0], self.height * 1.5 * Ratio[1])

    def on_press(self):
        global graphics
        if graphics.questmode or self.opacity == 0:
            return
        pos = (426 * Ratio[0], 420 * Ratio[1])
        angle = 0
        flipped = False
        for myShape in graphics.placed:
            if myShape.shapeid == self.shapeid:
                pos = myShape.pos
                angle = myShape.rot.angle
                flipped = myShape.flipped
                graphics.pc.removeShape(shape.shapes[myShape.shapeid])
                graphics.remove_widget(myShape)
                graphics.placed.remove(myShape)
                graphics.allShapes[myShape.shapeid - 1].opacity = 1
                break
        if graphics.currentShape:
            graphics.remove_widget(graphics.currentShape)
        graphics.currentShape = shapeImg(self.shapeid, pos, angle, flipped)
        self.onScreen = graphics.currentShape
        graphics.add_widget(graphics.currentShape)


class shapeImg(Image):

    def __init__(self, id, (x, y)=(426 * Ratio[0], 420 * Ratio[1]), angle=0, flipped=False):
        self.shapeid = id
        super(shapeImg, self).__init__()
        self.flipped = flipped
        self.shapePoints = copy.deepcopy(shape.shapes[self.shapeid])
        if self.flipped:
            self.source = FileLoc + 'Tomer KATAMINO\_' + str(self.shapeid) + 'f' + '.png'
            self.shapePoints.flip()
        else:
            self.source = FileLoc + 'Tomer KATAMINO\_' + str(self.shapeid) + '.png'
        self.pos = (x,y)
        self.keep_data = True
        self.opacity = 0.5

        if self.shapeid == 1:
            self.size = (SQUARE, SQUARE * 5)
        elif self.shapeid < 5:
            self.size = (SQUARE * 2, SQUARE * 4)
        else:
            self.size = (SQUARE * 3, SQUARE * 3)

        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            self.rot.angle = angle
            self.rot.origin = self.center
            self.rot.axis = (0, 0, 1)
        with self.canvas.after:
            PopMatrix()

    def move(self, dir):
        if dir == 'up':
            if self.center_y + self.size[1] / 2 + SQUARE< HEIGHT:
                self.center_y += SQUARE
        elif dir == 'down':
            if self.center_y - self.size[1] / 2 - SQUARE > 0:
                self.center_y -= SQUARE
        elif dir == 'right':
            if self.center_x + self.size[0] / 2 + SQUARE < WIDTH:
                self.center_x += SQUARE
        elif dir == 'left':
            if self.center_x - self.size[0] / 2 - SQUARE > 0:
                self.center_x -= SQUARE
        self.rot.origin = self.center

    def rotate(self):
        self.rot.origin = self.center
        if self.rot.angle + 90 == 360:
            self.rot.angle = 0
        else:
            self.rot.angle += 90

    def flip(self):
        if self.flipped:
            self.source = FileLoc + 'Tomer KATAMINO\_' + str(self.shapeid) + '.png'
            self.shapePoints.flip()
            self.flipped = False
        else:
            self.source = FileLoc + 'Tomer KATAMINO\_' + str(self.shapeid) + 'f' + '.png'
            self.shapePoints.flip()
            self.flipped = True

    def getArrayPos(self):
        pos = (int(round((self.pos[1] - 420 * Ratio[1]) / SQUARE)) + 1 - int(round(self.size[1] / SQUARE)), -int(round(((self.pos[0] - 426 * Ratio[0]) / SQUARE))))

        if self.shapeid == 6 or self.shapeid == 7:
                if self.rot.angle == 90:
                    pos = (pos[0] - 1, pos[1])
                elif self.rot.angle == 180:
                    pos = (pos[0], pos[1] - 1)

        elif self.shapeid <= 4 and self.shapeid >= 2:
            if self.rot.angle == 90 or self.rot.angle == 270:
                pos = (pos[0] - 1, pos[1] + 1)
            pos = (pos[0] + 2, pos[1])

        elif self.shapeid == 1:
            if self.rot.angle == 90 or self.rot.angle == 270:
                pos = (pos[0] - 2, pos[1] + 2)
            pos = (pos[0] + 4, pos[1])

        return pos

    def place(self):
        global graphics
        if graphics.pits(self):
            self.opacity = 1
            graphics.placed.append(self)
            graphics.allShapes[self.shapeid-1].opacity = 0.5
            graphics.currentShape = None
        if len(graphics.placed) == graphics.pc.numOfShapes:
            print "Won"
            graphics.add_widget(graphics.wonButton)



class Buffer(Image):

    def __init__(self, penta):
        super(Buffer, self).__init__()
        self.source = FileLoc + 'Tomer KATAMINO/buffer.png'
        self.penta = penta
        self.pos = (673 * Ratio[0] + SQUARE * (self.penta - 3), 390 * Ratio[1])
        self.size = (SQUARE, SQUARE * 5.75)

    def move(self, penta):
        self.penta = penta
        self.pos = (673 * Ratio[0] + SQUARE * (self.penta - 3), 390 * Ratio[1])


class QuestionButton(Button, Image):
    def __init__(self, text, pos=(100, 900)):
        super(QuestionButton, self).__init__()
        self.text = text
        self.pos = (pos[0] * Ratio[0], pos[1] * Ratio[1])
        self.size = (100 * Ratio[0], 100 * Ratio[1])
        self.font_size = 15 * Ratio[0]

    def on_press(self):
        global graphics
        if graphics.questmode:
            if self.text == 'Pick':
                if graphics.questSelect.questPlace:
                    graphics.addQuestion(graphics.questSelect.questPlace)
                graphics.remove_widget(self)
                graphics.remove_widget(graphics.returnButton)
                graphics.remove_widget(graphics.currentShape)
                graphics.currentShape = None
            else:
                graphics.remove_widget(self)
                graphics.remove_widget(graphics.pickButton)

            graphics.remove_widget(graphics.questSelect)
            graphics.questmode = False
        else:
            graphics.questmode = True
            graphics.add_widget(graphics.questSelect)
            graphics.add_widget(graphics.returnButton)
            graphics.add_widget(graphics.pickButton)
            graphics.questSelect.questPlace = None

class QuestionSelect(ButtonBehavior, Image):
    def __init__(self):
        super(QuestionSelect, self).__init__()
        self.source = FileLoc + 'Tomer KATAMINO/questiont.png'
        self.size = (WIDTH, HEIGHT)
        self.questPlace = None

    def on_touch_down(self, touch):
        pos = touch.pos
        pos = (pos[0] - 464 * Ratio[0], pos[1] - 168 * Ratio[1])
        self.questPlace = ((int)(6 - math.floor(pos[1]/(95 * Ratio[0]))), (int)(math.floor(pos[0]/(120 * Ratio[1]))))


class ClearButton(Button, Image):
    def __init__(self):
        super(ClearButton, self).__init__()
        self.text = 'Clear'
        self.pos = (1750 * Ratio[0], 900 * Ratio[1])
        self.size = (100 * Ratio[0], 100 * Ratio[1])
        self.font_size = 15 * Ratio[0]

    def on_press(self):
        global graphics
        graphics.clear()

class SolveButton(Button, Image):
    def __init__(self):
        super(SolveButton, self).__init__()
        self.text = 'Solve'
        self.pos = (1750 * Ratio[0], 750 * Ratio[1])
        self.size = (100 * Ratio[0], 100 * Ratio[1])
        self.font_size = 15 * Ratio[0]

    def on_press(self):
        global graphics
        graphics.start = timeit.default_timer()
        graphics.clear()
        if graphics.pc.solve(graphics.pc.shapes):
            # graphics.visualSolution()
            graphics.pc.printBoard()
            learn.add(graphics.pc.shapesOrder())
            learn.updateOrder()
            print("Program solved with " + str(ai.tries) + " tries in " + str("{:.2f}".format(timeit.default_timer() - graphics.start)) + " seconds")
            ai.tries = 1
        else:
            print "There is no solution to this problem"
        graphics.pc.clearBoard()

class WonButton(Button, Image):
    def __init__(self):
        super(WonButton, self).__init__()
        self.text = 'Good Job!'
        self.font_size = 50 * Ratio[0]
        self.size = (400 * Ratio[0], 400 * Ratio[1])
        self.center = (WIDTH / 2, HEIGHT / 2)

    def on_press(self):
        global graphics
        graphics.remove_widget(self)

class KataminoApp(App):
    def build(self):
        return graphics


graphics = Graphics()

if __name__ == '__main__':
    KataminoApp().run()
    pickle_out = open("learning.pickle", "wb")
    cPickle.dump(learn, pickle_out)
    pickle_out.close()