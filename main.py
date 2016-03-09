#encoding=utf-8
import sudoku1,sudoku2
import sys
import time,copy
import string
from readproblem import fread_problem
mode=1
if __name__ == "__main__":
    if len(sys.argv)>1:
        mode=1 if sys.argv[1]==1 else 2
    lProblemList=fread_problem('Sudoku_input.txt')
    count=0
    print("Start solving..(MODE %d)"%mode)
    for lProblem in lProblemList:
        count=count+1
        startTime=time.time()
        ###
        if(mode==2):
            sodu=sudoku2.SodukuStack(lProblem)
            sodu.resolve()
        else:
            sodu=sudoku1.SodukuStack(lProblem)
            sodu.resolve()
        ###
        endTime=time.time()
        useTime=endTime-startTime
        print ("  Problem " + "%d" % count + ": finished!\nTime consuming: " + "%.4f" %useTime + " Seconds\n")
        rlt=True
        if (mode==2):
            rlt=sodu.is_right
        else:
            rlt=sodu.current.is_right()
        if not rlt:
            print("No Answer...")
        else:
            if (mode==2):
                sodu.display()
            else:
                sodu.current.arr.display()
    print("Done!!")
