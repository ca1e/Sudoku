#!/usr/bin/python
#encoding=utf-8
import time
import copy
from readproblem import read_problem

class Matrix(list):
    """�����࣬��Ҫ��list�Ļ�����ʵ��get_row,get_col�ȹ���"""

    def get_grid(self,x,y,with_zero = False):
        """��ȡԪ������С�Ź��������е�����"""
        g = lambda x:x-(x)%3
        x,y = g(x),g(y)
        if with_zero:
            return [b[a] for b in self[y:y+3] for a in range(x,x+3)]
        else:
            return [b[a] for b in self[y:y+3] for a in range(x,x+3) if not b[a] == 0]
 
    def get_row(self, y):
        return self[y]
 
    def get_col(self, x):
        return [a[x] for a in self]
 
    def rows(self):
        for y in range(0,9):
            yield self[y]

    def display(self):
        """��ӡ����"""
        for l in self:
            outLine=''
            for number in l:
                outLine=outLine + "%d" % number +' '
            print(outLine)

class Soduku(object):
    arr = Matrix
    snapshot = []
    candidacy = Matrix([[0]*9 for i in range(0,9)])
    ref = set(range(1,10))
    grid_ref = [(x,y) for x in range(0,9,3) for y in range(0,9,3)]
    def __init__(self, arr):
        self.arr = Matrix(arr)
        self.snapshot = []
        self.create_cand()
    def loop(self):
        """����һ����󣬽�����ȷ����ֵ��д������ʽΨһ��"""
        for y,row in enumerate(self.candidacy):
            for x,col in enumerate(row):
                if type(col) == set and len(col) == 1:
                    self.arr[y][x] = col.pop()
                    self.candidacy[y][x] = 0
                    self.update_cand()
        self.update_cand()
 
    def create_cand(self):
        """������ѡ������"""
        for y,row in enumerate(self.arr):
            for x,col in enumerate(row):
                if col == 0:
                    result = self.search_available(x,y)
                    self.candidacy[y][x] = result
                else:
                    self.candidacy[y][x] = 0
 
    def update_cand(self):
        """���º�ѡ������"""
        for y,row in enumerate(self.candidacy):
            for x,col in enumerate(row):
                if type(col) == set:
                    avai = self.search_available(x,y)
                    if avai:
                        self.candidacy[y][x] = avai
                    else:
                        self.candidacy[y][x] = 0
    def search_available(self, x ,y):
        """���x,y��Ӧ��λ�õ����п��������"""
        set_a = self.ref.difference(self.arr.get_row(y))
        set_b = self.ref.difference(self.arr.get_col(x))
        set_c = self.ref.difference(self.arr.get_grid(x,y))
        return set_a.intersection(set_b,set_c)
 
    def search_unique(self):
        """��ʽΨһ��ɨ��"""
        #����ɨ��
        for y in range(0,9):
            num = self.count(*self.candidacy[y])
            if num:
                self.arr[y][num[1]] = num[0]
                self.candidacy[y][num[1]] = 0
                self.update_cand()
        #����ɨ��
        for x in range(0,9):
            num = self.count(*self.candidacy.get_col(x))
            if num:
                self.arr[num[1]][x] = num[0]
                self.candidacy[num[1]][x] = 0
                self.update_cand()
        #������ɨ��
        for x,y in self.grid_ref:
            num = self.count(*self.candidacy.get_grid(x,y,with_zero=True))
            if num:
                self.arr[y+num[1]/3][x+num[1]%3] = num[0]
                self.candidacy[y+num[1]/3][x+num[1]%3] = 0
                self.update_cand()
    def count(self,*args):
        """ͳ��ֻ����һ�ε����֣��������ֱ�����λ��"""
        l = []
        for i,d in enumerate(args):
            if type(d) == set:
                l.extend(d)
        for i in range(1,10):
            if l.count(i) == 1:
                unique = i
                for j,d in enumerate(args):
                    if type(d) == set and unique in d:return (unique,j)
        return 0

    def is_complete(self):
        """�����û��δ�����"""
        for y in self.arr:
            for x in y:
                if x == 0:  return False
        return True

    def is_right(self):
        """���С��С�����ɨ�裬����Ƿ񶼰���1-9�Ÿ�����"""
        for y in self.arr:
            if not set(y) == self.ref:
                return False
        for x in range(0,9):
            if not set(self.arr.get_col(x)) == self.ref:
                return False
        for x,y in self.grid_ref:
            if not set(self.arr.get_grid(x,y)) == self.ref:
                return False
        return True

    def has_error(self):
        """�жϵ�ǰ״̬��û�д���"""
        tmp = []
        #��ĳһδ��ĸ�����Ӧ�ĺ�ѡ��Ҳ������ʱ���϶�Ϊ�д���
        for y in range(0,9):
            for x in range(0,9):
                if self.arr[y][x] == 0 and self.candidacy[y][x] == 0:   return True
        #ɨ�����С�����û���ظ�ֵ
        for y in range(0,9):
            for element in self.arr[y]:
                if element and element in tmp:
                    return True
                tmp.append(element)
            del tmp[:]
        for x in range(0,9):
            col = self.arr.get_col(x)
            for element in col:
                if element and element in tmp:  return True
                tmp.append(element)
            del tmp[:]
        return False

    def resolve(self):
        while self.arr != self.snapshot:
            #ÿ��Ϊ��������һ�ο���
            self.snapshot = copy.deepcopy(self.arr)
            self.loop()
            self.search_unique()

class SodukuStack(object):
    stack = []
    candidacy = []
    deep = 0

    def __init__(self, arr):
        self.current = Soduku(arr)
        self.current.resolve()
        self.stack.append(self.current)
        self.candidacy.append(self.padding(self.current))

    def resolve(self):
        while not self.current.is_complete() or not self.current.is_right():
            try:
                self.foward()
            except IndexError:
                if self.deep > 0: 
                    #�������п��ܺ�ֱ�ӻع��������
                    self.rollback()
                    continue
                else:
                    print("the Soduku can't be sloved")
                    break
            if self.current.has_error():
                self.rollback()

    def foward(self):
        """����һ�����ܵ�����"""
        x,y = self.candidacy[self.deep]['position']
        newarr = copy.deepcopy(self.current.arr)
        newarr[y][x] = self.candidacy[self.deep]['candidacy'].pop()
        self.stack.append(Soduku(newarr))
        self.deep += 1
        self.current = self.stack[self.deep] 
        self.current.resolve()
        self.candidacy.append(self.padding(self.current))

    def rollback(self):
        """�ع����ָ�δ���Ե�״̬"""
        self.stack.pop()
        self.candidacy.pop()
        self.deep -= 1
        self.current = self.stack[self.deep]
    
    def padding(self, obj):
        """��ÿ��õ�����ѡ������λ��"""
        for py,y in enumerate(obj.candidacy):
            for px,x in enumerate(y):
                if x:
                    candidacy = list(x)
                    return {
                        'candidacy': candidacy,
                        'position': (px,py)
                    }       


if __name__ == "__main__":
    lProblemList=read_problem('Sudoku_input.txt')
    count=0
    print "Start solving.."
    for lProblem in lProblemList:
        count=count+1
        startTime=time.time()
        array1 = Matrix(lProblem)
        #array1.display()
        sodu = SodukuStack(array1)
        sodu.resolve()
        endTime=time.time()
        useTime=endTime-startTime
        print "  Problem " + "%d" % count + ": finished!\nTime consuming: " + "%.4f" %useTime + " Seconds\n"
        if not sodu.current.is_right():
            print("No Answer...")
        else:
            sodu.current.arr.display()
    print "Done!!"      