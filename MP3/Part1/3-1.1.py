# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 00:56:21 2018

@author: JAD
"""
import math
import numpy as np
import matplotlib.pyplot as plt
#np.set_printoptions(threshold=np.inf)  
traindict = {}
np_start0 = np.zeros(32*32+1)
np_start1 = np.zeros(32*32+1)
np_start2 = np.zeros(32*32+1)
np_start3 = np.zeros(32*32+1)
np_start4 = np.zeros(32*32+1)
np_start5 = np.zeros(32*32+1)
np_start6 = np.zeros(32*32+1)
np_start7 = np.zeros(32*32+1)
np_start8 = np.zeros(32*32+1)
np_start9 = np.zeros(32*32+1)

traindict[0] = np_start0
traindict[1] = np_start1
traindict[2] = np_start2
traindict[3] = np_start3
traindict[4] = np_start4
traindict[5] = np_start5
traindict[6] = np_start6
traindict[7] = np_start7
traindict[8] = np_start8
traindict[9] = np_start9
traindict[0][0]+=1

def showplt(k, traindict):
    np0 = np.zeros((32,32))
    for i in range(0,32):
        for j in range(0,32):
            np0[i][j] = traindict[k][i*32+j]
    plt.matshow(np0, cmap = 'hot')
    plt.colorbar()
    plt.show()

with open('optdigits-orig_train.txt') as f:
        train_data_temp = []
        for y, line in enumerate(f):
            row = []
            for x, num in enumerate(line):
                if(num=='\n'):
                    break
                if(num=='0'):
                    row.append(0.0)
                if(num=='1'):
                    row.append(1.0)
                if(num=='2'):
                    row.append(2.0)
                if(num=='3'):
                    row.append(3.0)
                if(num=='4'):
                    row.append(4.0)
                if(num=='5'):
                    row.append(5.0)
                if(num=='6'):
                    row.append(6.0)
                if(num=='7'):
                    row.append(7.0)
                if(num=='8'):
                    row.append(8.0)
                if(num=='9'):
                    row.append(9.0)
            train_data_temp.append(row)
        train_data = np.array(train_data_temp)

with open('optdigits-orig_test.txt') as f:
        test_data_temp = []
        for y, line in enumerate(f):
            row = []
            for x, num in enumerate(line):
                if(num=='\n'):
                    break
                if(num=='0'):
                    row.append(0.0)
                if(num=='1'):
                    row.append(1.0)
                if(num=='2'):
                    row.append(2.0)
                if(num=='3'):
                    row.append(3.0)
                if(num=='4'):
                    row.append(4.0)
                if(num=='5'):
                    row.append(5.0)
                if(num=='6'):
                    row.append(6.0)
                if(num=='7'):
                    row.append(7.0)
                if(num=='8'):
                    row.append(8.0)
                if(num=='9'):
                    row.append(9.0)
            test_data_temp.append(row)
        test_data = np.array(test_data_temp)

total_len = len(train_data)

for i in range(0, int(total_len/33)):
    cur_num = train_data[(i+1)*33-1][0]
    for j in range(0, 32):
        for k in range(0,32):
            traindict[cur_num][j*32+k-1]+=train_data[i*33+j][k]
    traindict[cur_num][31*32+32]+=1

for i in range (0,10):
    for j in range (0, 32*32):
        traindict[i][j] = (traindict[i][j]+1)/(traindict[i][32*32]+2)
    traindict[i][32*32]/=total_len

def guess(num):
    record = np.zeros(10)
    for i in range(0,10):
        record[i] = math.log(traindict[i][-1])
    
    for i in range (0,32):
        for j in range (0,32):
            for k in range (0,10):
                if test_data[33*num+i][j] == 1:
                    record[k] += math.log(traindict[k][i*32+j-1])
                else:
                    record[k] += math.log(1-traindict[k][i*32+j-1])
    
    max = -999999
    maxi = 1
    for i in range(0,10):
        #print(record[i])
        if record[i]>max:
            max = record[i]
            maxi = i

    return maxi

def test(num):
    guessing  = guess(num)
    true_val = test_data[33*num+32][0]
    if guessing==true_val:
        return True
    else:
        return False

confusion_matrix = np.zeros((10,10))
for i in range(0, int(len(test_data)/33)):
    true_val = test_data[33*i+32][0]
    guess_val = guess(i)
    confusion_matrix[int(true_val)][int(guess_val)]+=1

print(confusion_matrix)
'''
record = np.zeros(10)
#print(math.log10(10))

for i in range(0,10):
    record[i] = math.log(traindict[i][-1])

for i in range (0,32):
    for j in range (0,32):
        for k in range (0,10):
            if test_data[33+i][j] == 1:
                record[k] += math.log(traindict[k][i*32+j-1])
            else:
                record[k] += math.log(1-traindict[k][i*32+j-1])

max = -999999
maxi = 1
for i in range(0,10):
    print(record[i])
    if record[i]>max:
        max = record[i]
        maxi = i

print(maxi)
'''
#showplt(0,traindict)    
    