import pandas as pd
import numpy as np
import math
import json
from pprint import pprint

def parameterReader(file='try.json'):
    with open('try.json') as f:
        data = json.load(f)

    #print(data)
    data['bucketting'][0]['Too dense']
    hyperparameters=[data['bucketting'][0]['Per Unique Values'],
                 data['bucketting'][0]['empty bucket percentage of data'],
                 data['bucketting'][0]['No of empty buckets for clustered data'],
                 data['bucketting'][0]['Too dense'],
                 data['bucketting'][0]['max no of parts for bucket'],
                 data['bucketting'][0]['max no of zeros']]
    return hyperparameters

def unique(array):
    unique_list = []
    for x in array:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def buckets(array,hyperParameters=parameterReader()):
    
    # If per unique element ratio is less than the particular ratio, classify it as a step data.
    
    if (len(unique(array))/len(array)<1/hyperParameters[0]):
        print('Step data')
        return steps(array)
    
    #Divided data in 100 parts according to range
    
    parts100=pd.cut(sorted(array),100)
    
    #Making list of the intervals
    intervals = [[a.left,a.right] for a in parts100.categories]
    binno=0
    empty=0
    
    while binno<100:
        if parts100.value_counts()[binno]/len(array)<hyperParameters[1]:
            empty+=1
        binno+=1
        
    #If number of empty bins(I will refer every 100th division as 'bins') are more than the required,make it clustered data  
    if empty>hyperParameters[2]:
        print('clustered data')
        return cluster(array,hyperParameters)
    
    #If none satisfied, the data has continuous type of distribution
    print('continuous data')
    return continuous(array) 



#Directly taking every element as a category
def steps(array):
    return array  



def cluster(array,hyperParameters=parameterReader()):
    parts100=pd.cut(array,100)
    bins = [[a.left,a.right] for a in parts100.categories]
    binno=0
    bucket=[]
    intervals=[min(array)]
    while binno<100:
        minv=bins[binno][0]
        zeroParts=0
        dens=0
        parts=0
        
        # Adding bin to the bucket till:
        # 1)Maximum no of empty bins allowed is not reached.
        # 2)Density of bucket is less than the specified density.
        # 3)No of bins in a bucket is less than the specified count.
        
        while (parts<hyperParameters[4] and dens<hyperParameters[3] and zeroParts<hyperParameters[5] and binno<100):
            if parts100.value_counts()[binno]/len(array)<hyperParameters[1]:
                zeroParts+=1
            else:
                dens+=(parts100.value_counts()[binno]/len(array))
            parts+=1
            binno+=1     
            
        maxv=bins[binno-1][1]
        
        intervals.append(maxv)
        
        #Making a list of limits of bucket
        bucket.append([minv,maxv])

    intervals[-1]=intervals[-1]+1
    
    #Replacing array element by its bucket
    
    x=list(np.digitize(array, intervals) - 1)
    newx=[]
    for i in range(len(x)):
        newx.append(bucket[x[i]])

        #Returning newly made array with categories instead of integers. 
    return newx
    
def continuous(array):
    
    # Divided data by quantiles.
    quart=pd.qcut(array,4)
    intervals = [[a.left,a.right] for a in quart.categories]
    vals=[]
    binParam=[]
    
    
    for i in range(len(intervals)):
        buck=[a for a in array if intervals[i][0]<=a<intervals[i][1]]
        vals.append(buck)
    for j in range(0,4):
        binSize=max(vals[j])-min(vals[j])
        b=binSize/math.sqrt(len(vals[j]))
        binParam.append(b)
        
###################       
    # Selecting the bin parameter (bin size/square root of number of elements) 
###################   
    size=(min(binParam))                                         
    # Next operation will give us bucket size
    nb=math.ceil((max(array)-min(array))/size)
    
    # Divide data by the calculated bucket size
    bins=pd.cut(array,nb)
    buckets = [[a.left,a.right] for a in bins.categories]
    ranges=[a.right for a in bins.categories]
    ranges.append(min(array))
    ranges=sorted(ranges)
    ranges[-1]=ranges[-1]+1
    
    #Replacing array element by its bucket

    x=list(np.digitize(array, ranges) - 1)
    newx=[]
    for i in range(len(x)):
        newx.append(buckets[x[i]])
            
            #Returning newly made array with categories instead of integers. 
    return newx
