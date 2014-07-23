# Author : Ekta Grover
# 10/04/2014
# Refresh intervals against count of instances by users 


#from __future__ import division
from pylab import *
import pandas  as pd , csv
import matplotlib.pyplot as plt
from matplotlib import rc
import random
import numpy as np
from itertools import chain #list(chain.from_iterable(x)
from itertools import izip, islice
import operator
#placing anchored text within the figure
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
rc('mathtext', default='regular')
import pickle # to dump objects in a text file
from collections import Counter #Counter(z), where z is a (flat)list
from itertools import tee, islice, chain, izip


filehandle1="C:/Users/Ekta.Grover/Desktop/Dynamic Bidding/latest data/latest data/ARI/ios_skout_new_multiple_COMPLETE.tsv"
filehandle2="C:/Users/Ekta.Grover/Desktop/Dynamic Bidding/latest data/latest data/ARI/ios_skout_new_multiple_COMPLETE_CSV.csv"


def tsv_to_csv(filehandle1, filehandle2) :  
    input_file=open(filehandle1,"rb")
    output_file = open(filehandle2, "wb")
    num_lines = sum(1 for line in  open(filehandle1,"rb"))
    tabin = csv.reader(input_file, dialect=csv.excel_tab)
    commaout = csv.writer(output_file, dialect=csv.excel)
    for row in tabin:
        commaout.writerow(row)
    print "Done writing the csv file"
    output_file.close()
    del input_file,output_file,commaout,tabin 
    return num_lines, filehandle2

#num_lines, filehandle2=tsv_to_csv(filehandle1, filehandle2)
df = pd.read_csv(filehandle2,skiprows=0, sep=',')
print "read into df"

# post this just read all the diff in times for "A" users & aggregate them over all, & finally plot them
# ARI =1, agianst count etc.


def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(prevs, items, nexts)


p=list(set(df['user']))
len(p)
d_ARI={}
d_ARI_diff={}
for key in p[0:10]:
    d_ARI[key]=list(df[df['user']==key]['etime']) # let's remove elements outright from the substraction?
    temp=[]
    for previous, item, nxt in previous_and_next(d_ARI[key]):
        if nxt :
            temp.append(nxt-item)
        temp= [s for s in temp if s <=2*60]# plotting on a 2 minute window only
    d_ARI_diff[key]=temp
"""
# this was not scalable
    for  next_item,current_item in izip(islice(the_list, 1, None),the_list):
        temp.append(next_item-current_item)
    d_ARI_diff[key]=temp
val=[]
"""
val=[]
for items in d_ARI_diff.values():
# unchain & count the items in this list 
    val.append(items)
val=list(chain.from_iterable(val))
z=Counter(val)
x=z.keys()
y=z.values()
[x, y] = zip(*sorted(zip(x, y), key=lambda x: x[0])) ###

xlim([min(x),max(x)])
ylim([min(y),max(y)])
appname=filehandle1.split("/")[-1].replace("_multiple_COMPLETE.tsv","")
title='\n Distribution of Average session depth wrt number of users \n Data considered only over a 2 minute  window \n on App :'+str(appname)
plt.suptitle(title, fontsize=12)
plt.ylabel('Number of instances(beonging to users) having that Refresh interval' ) 
plt.xlabel('Refresh interval in seconds')
plt.plot(x, y, '-',color='r')
#plt.show()

savepath="C:/Users/Ekta.Grover/Desktop/Dynamic Bidding/latest data/latest data/ARI/instances_ASD_counts_"+appname+".png"
plt.savefig(savepath,bbox_inches='tight')
plt.close()
print "Execution over"


