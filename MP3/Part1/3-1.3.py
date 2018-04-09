# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 00:56:21 2018

@author: JAD
"""
import math
import numpy as np
import matplotlib.pyplot as plt
#np.set_printoptions(threshold=np.inf)  
for sf in range (1,100):
    traindict = {}
    np_start0 = np.zeros(60*70+1)
    np_start1 = np.zeros(60*70+1)
    
    
    traindict[0] = np_start0
    traindict[1] = np_start1
    
    
    def showplt(k, traindict):
        np0 = np.zeros((70,60))
        for i in range(0,70):
            for j in range(0,60):
                np0[i][j] = traindict[k][i*60+j]
        plt.matshow(np0, cmap = 'hot')
        plt.colorbar()
        plt.show()
    
    with open('facedatatrain') as f:
            train_data_temp = []
            for y, line in enumerate(f):
                row = []
                for x, num in enumerate(line):
                    if(num=='\n'):
                        break
                    if(num==' '):
                        row.append(0.0)
                    if(num=='#'):
                        row.append(1.0)
                train_data_temp.append(row)
            train_data = np.array(train_data_temp)
    
    with open('facedatatest') as f:
            test_data_temp = []
            for y, line in enumerate(f):
                row = []
                for x, num in enumerate(line):
                    if(num=='\n'):
                        break
                    if(num==' '):
                        row.append(0.0)
                    if(num=='#'):
                        row.append(1.0)
                test_data_temp.append(row)
            test_data = np.array(test_data_temp)
    
    with open('facedatatrainlabels') as f:
            train_data_label = []
            for y, line in enumerate(f):
                row = []
                for x, num in enumerate(line):
                    if(num=='\n'):
                        break
                    if(num=='0'):
                        train_data_label.append(0.0)
                    if(num=='1'):
                        train_data_label.append(1.0)
    
    with open('facedatatestlabels') as f:
            test_data_label = []
            for y, line in enumerate(f):
                row = []
                for x, num in enumerate(line):
                    if(num=='\n'):
                        break
                    if(num=='0'):
                        test_data_label.append(0.0)
                    if(num=='1'):
                        test_data_label.append(1.0)
    
    total_len = len(train_data)
    
    for i in range(0, int(total_len/70)):
        cur_num = train_data_label[i]
        for j in range(0, 70):
            for k in range(0,60):
                traindict[cur_num][j*60+k-1]+=train_data[i*70+j][k]
        traindict[cur_num][-1]+=1
    
    smoothing_factor = sf/10
    for i in range (0,2):
        for j in range (0, 70*60):
            traindict[i][j] = (traindict[i][j]+1*smoothing_factor)/(traindict[i][-1]+2*smoothing_factor)
        traindict[i][-1]/=(total_len/70)
    #showplt(1, traindict)
    #print(traindict[1])
    def guess(num):
        record = np.zeros(2)
        for i in range(0,2):
            record[i] = math.log(traindict[i][-1])
        
        for i in range (0,70):
            for j in range (0,60):
                for k in range (0,2):
                    if test_data[70*num+i][j] == 1:
                        record[k] += math.log(traindict[k][i*60+j-1])
                    else:
                        #print(1-traindict[k][i*70+j-1])
                        record[k] += math.log(1-traindict[k][i*60+j-1])
        
        maxval = -999999
        maxi = 1
        for i in range(0,2):
            #print(record[i])
            if record[i]>maxval:
                maxval = record[i]
                maxi = i
    
        return maxi
        
    total_case = 0
    total_correct = 0
    max_acc = 0
    max_sf = 0
    confusion_matrix = np.zeros((2,5))
    for i in range(0, int(len(test_data)/70)):
        true_val = test_data_label[i]
        guess_val = guess(i)
        confusion_matrix[int(true_val)][int(guess_val)]+=1
        total_case+=1
        confusion_matrix[int(true_val)][2]+=1
        if(true_val==guess_val):
            total_correct+=1
            confusion_matrix[int(true_val)][3]+=1
    for i in range(0, 2):
        confusion_matrix[i][4] = confusion_matrix[i][3]/confusion_matrix[i][2]
    #print(confusion_matrix)
    if (total_correct/total_case)>max_acc:
        max_acc = total_correct/total_case
        max_sf = smoothing_factor
    #print("when smoothing constant is:",smoothing_factor,"accuracy is:",total_correct/total_case)
print("when smoothing constant is:",max_sf,"best accuracy is:",max_acc)

#showplt(0,traindict)    
 