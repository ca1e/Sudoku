#encoding=utf-8
import copy

#从文件中读取数独问题，每题之间用";"分隔,各数字之间用空格分隔
ignorechar=('#')

def read_problem(filename):
    inputFile=open(filename,'r')
    rtnList=[]
    lP=[]
    ignor=False
    while True:
        line=inputFile.readline()
        line=line.strip()
        if len(line) == 0:
            break
        if line[0]=='{':
            ignor=True
            continue
        if line[0]=='}':
            ignor=False
            continue
        if line[0] in ignorechar or ignor:
            continue
        if line == ';':
            if len(lP)==9:
                rtnList.append(copy.deepcopy(lP))
            lP=[]
            continue
        if len(line)==161:
            rowL=line.split(',')
            rowList=[]
            for i in rowL:
                rowList.append(int(i))
            for a in [i for i in range(73) if i%9==0]:
                lP.append(rowList[a:a+9])
            rtnList.append(copy.deepcopy(lP))
            lP=[]
            continue
            
        rowList=line.split(' ')
        numberList=[]
        for number in rowList:
            try:
                number = int(number)
                if number<10 and number>=0 :
                    numberList.append(number)
            except:
                continue
        if len(numberList)==9:
            lP.append(numberList)
    return rtnList