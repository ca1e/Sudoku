#!/usr/bin/python
# -*- coding:utf-8 -*-
import string
import copy
import time
from readproblem import read_problem

#����������
# lProblem:�������⣬��һ����ά�����ʾ
# logFile: ��־�ļ�������������������ļ���   
def sudoku_solver(lProblem):
    lSolverStack=[lProblem]
    count=0
    # ����ջ��Ϊ�գ���ѭ��
    while len(lSolverStack)>0:
        lCurrSolution=lSolverStack.pop()
        count=count+1
        for row in lCurrSolution:
            outLine=''
            for number in row:
                outLine=outLine + "%d" % number +' '
        isResult=True
        #���ڴ�ŵ�ǰ���ٺ�ѡ���б�
        lMinAvailableNumber=range(1,10)
        #��ǰ���ٺ�ѡ������λ��
        lMinAvailableNumberX=0
        lMinAvailableNumberY=0
       
        for idx in range(81):
            i=idx%9
            j=idx/9
            if lCurrSolution[i][j]==0:
                isResult=False
                #���㵱ǰλ�ÿ��Է��õ������б�
                lCurrAvailableNumber=range(1,10)
                #���ͬһ���д�����ͬԪ�أ����ų�
                for x in range(9):
                    if lCurrAvailableNumber.count(lCurrSolution[i][x])>0:
                        lCurrAvailableNumber.remove(lCurrSolution[i][x])
                #���ͬһ���д�����ͬԪ�أ����ų�
                for y in range(9):
                    if lCurrAvailableNumber.count(lCurrSolution[y][j])>0:
                        lCurrAvailableNumber.remove(lCurrSolution[y][j])
                #�����ǰλ�����ڵ�С�Ź����д�����ͬԪ�أ����ų�
                for x in range(i/3*3,i/3*3+3):
                    for y in range(j/3*3,j/3*3+3):
                        if lCurrAvailableNumber.count(lCurrSolution[x][y])>0:
                            lCurrAvailableNumber.remove(lCurrSolution[x][y])
                #�����ǰ��Ԫ���п�ѡ���ָ������٣�����           
                if len(lCurrAvailableNumber)<len(lMinAvailableNumber):
                    lMinAvailableNumber=copy.deepcopy(lCurrAvailableNumber)
                    lMinAvailableNumberX=i
                    lMinAvailableNumberY=j
               
                if len(lMinAvailableNumber)==0:
                    break
               
        #����ǰλ�ô��ڿ�ѡ���֣��򽫵�ǰλ�õ����п�ѡ���֣�������Ϊ��ʱ�⣬�������ջ
        if len(lMinAvailableNumber)>0:
            for number in lMinAvailableNumber:
                lNewSolution=copy.deepcopy(lCurrSolution)
                lNewSolution[lMinAvailableNumberX][lMinAvailableNumberY]=number
                lSolverStack.append(lNewSolution)       
               
        if isResult:
            return lCurrSolution
    return []

def showsudoku(s):
        """��ӡ����"""
        for row in s:
            outLine=''
            for number in row:
                outLine=outLine + "%d" % number +' '
            print(outLine)  
       
if __name__ == '__main__':
    lProblemList=read_problem('Sudoku_input.txt')
    count=0
    print "Start solving.."
    for lProblem in lProblemList:
        count=count+1
        startTime=time.time()
        lResult=sudoku_solver(lProblem)
        endTime=time.time()
        useTime=endTime-startTime
        print "  Problem " + "%d" % count + ": finished!\nTime consuming: " + "%.4f" %useTime + " Seconds\n"
        if len(lResult)==0:
            print("No Answer...")
        else:
            showsudoku(lResult)
    print "Done!!"