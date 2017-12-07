import cPickle
import questions
import ai
import timeit

pickle_in = open("learning.pickle", "rb")
learn = cPickle.load(pickle_in)

def main():


    pc = ai.Ai(questions.getSlamQuestion(0,9))
    start = timeit.default_timer()
    if pc.solve(pc.shapes):
        pc.printBoard()
        learn.add(pc.shapesOrder())
        learn.updateOrder()
        stop = timeit.default_timer()
        print("Program solved with " + str(ai.tries) + " tries in " + str("{:.2f}".format(stop - start)) + " seconds")
    else:
        print "There is no solution to this problem"

    print learn.bestOrder

    pickle_out = open("learning.pickle", "wb")
    cPickle.dump(learn, pickle_out)
    pickle_out.close()

if __name__ == "__main__":
    main()