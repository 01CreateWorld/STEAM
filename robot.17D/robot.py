import os
import re
import sys
import time

def actAnalys(actionStr):    
    #匹配舵机动作时间字符串
    actRegex=re.compile(r'T\d{3,4}')
    actTime=actRegex.search(actionStr).group()

    #匹配舵机角度字符串，并放入列表
    actRegex=re.compile(r'#\d{1,2}P\d{3,4}')
    actServos=actRegex.findall(actionStr)
    #print (action+'\n'+ actTime+'\n'+actServos[0])

    #从舵机角度列表，逐个舵机匹配舵机号和角度
    servoNo=[]
    servoAngle=[]

    for actServo in actServos:
        actRegex=re.compile(r'#\d{1,2}')
        servoNo.append( actRegex.search(actServo).group() )

        actRegex=re.compile(r'P\d{3,4}')
        servoAngle.append(int( actRegex.search(actServo).group().replace('P','') )) 

    actDict={'actTime':actTime,'servoNo':servoNo,'servoAngle':servoAngle}
    return actDict

#原始站立文件stand0.txt，读一行，去掉空白字符，用actAnalys()分析
actfile=open('stand0.txt')
line = actfile.read().strip()
if len(line)>0:
    stand0 = actAnalys(line)
    
else:
    print ('原始站立文件是空的！')

actfile.close()

#当前站立文件stand1.txt，读一行，去掉空白字符，用actAnalys()分析    
actfile=open('stand1.txt')
line = actfile.read().strip()
if len(line)>0:
    stand1 = actAnalys(line)
    
else:
    print ('原始站立文件是空的！')

actfile.close()

#动作文件xxx.txt，读多行，逐行，去掉空白字符，用actAnalys()分析    
print('\n请输入源动作文件名，不用加.txt，将自动加上.txt后缀：\n')
fileName = input('你需要批量修改的源动作文件：')
if len(fileName)==0:
    print('你没有输入任何的文件名.')
    sys.exit(0)
else:
    file4Read = fileName+'.txt'
    try:
        actfile=open(file4Read)
    except:
        print('打开文件时发生错误.这个文件存在吗？')
        sys.exit(1)

lines = actfile.readlines()
if len(lines)>0:
    actions0=[]
    for line in lines:
        actions0.append( actAnalys(line) )
    
else:
    print ('原始站立文件是空的！')

actfile.close()

#计算新的动作，原动作列表逐项，与原始站立动作比较（计算差值），与新站立文件叠加（加上新站立动作的角度）
#动作列表的每一项为一项字典，字典中每一个舵机的角度，逐个计算
actions1=[]
for actDict0 in actions0:
    actDict1={}
    actDict1['actTime']=actDict0['actTime']
    i=0
    servoAngle=[]
    while i<len(actDict0['servoNo']):
        if actDict0['servoNo'][i] == stand0['servoNo'][i] and actDict0['servoNo'][i] == stand1['servoNo'][i] :
            servoAngle.append( actDict0['servoAngle'][i] - stand0['servoAngle'][i] + stand1['servoAngle'][i] )
        i+=1

    actDict1['servoNo']=actDict0['servoNo']
    actDict1['servoAngle']=servoAngle

    actions1.append(actDict1)

actions1.append( stand1 )

#将新动作列表逐项，转化为字符串，写入文件
timeStr=time.strftime("%Y%m%d%H%M%S", time.localtime())
file4Write=fileName + timeStr + '.txt'

actfile=open(file4Write,mode='w')
for actDict1 in actions1:
    i = 0
    line=''
    while i < len(actDict1['servoNo']):
        line += actDict1['servoNo'][i]
        line += 'P'
        line += str(actDict1['servoAngle'][i])
        i += 1
    line += actDict1['actTime']
    line += '\n'
    actfile.write(line)
actfile.close()

pass