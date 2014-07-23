# final file for in -app-anlalysis - need to clean this up 
# Ekta Grover : 09/05/2014

# count of ARI against users
# retry for optimization
#from __future__ import division
#from datetime import datetime
#startTime = datetime.now()
from multiprocessing.dummy import Pool as ThreadPool
from pylab import *
import time
import gc
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
start = time.time()


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

def other_processing(filehandle2,appname,cutoff):
    df = pd.read_csv(filehandle2,skiprows=0,sep=',' ,nrows=1000000)
    #df = pd.read_csv(filehandle2,skiprows=0,sep=',',,usecols=["user","etime"],nrows=1000)#,nrows=1000)#,usecols=["user","etime"], sep=',') #,nrows=50000)
    p=list(set(df['user']))
    #print "printing keys in p"
    #print p[0:10]
    #print "read into df"
    z1={}
    i=0
    for m in range(0,cutoff+1):
        z1[m]=0
    z1[0]=sum(df['count'])
    df=df[["user","etime"]]
    for key in p[0:10]:
        the_list=sorted(list(df[df['user']==key]['etime']))
        df=df.drop(df.index[df['user']==key])
        for  next_item,current_item in izip(islice(the_list, 1, None),the_list):
            if (next_item-current_item)<=(cutoff) and (next_item-current_item) >0 :
                z1[next_item-current_item]=z1[next_item-current_item]+1
        del the_list
    x=z1.keys()
    y=list(log(z1.values()))
    del z1,df
    [x, y] = zip(*sorted(zip(x, y), key=lambda x: x[0])) 
    xlim([min(x),max(x)])
    ylim([min(y),max(y)])
    x,y=list(x),list(y)
    max_xy=local_maxima(x, y)
    x1=[x[i] for i in max_xy]
    y1=[y[i] for i in max_xy]
    for i in range(0,len(x1)):
        if x1==0:
            pass
        else :
            txt = x1[i]#,y1[i])
            plt.annotate(str(txt),(x1[i],y1[i]))
    appname=appname.split('_new_logic')[0]
    title='\n Distribution of Average session depth wrt number of users \n Data considered only over a '+str(cutoff)+'seconds window \n on App :'+str(appname)
    plt.suptitle(title, fontsize=12)
    plt.ylabel('Number of instances(belonging to users='+str(len(p))+')\n having that Refresh interval \n log scale' ) 
    plt.xlabel('Refresh interval in seconds')
    plt.plot(x, y, '-',color='r')
    savepath="/home/ekta/Desktop/BACKUP/DynamicBidding/latestData/latestData/ARI/Newdata1504/time_diff_analysis/Finding_Peaks/folder2/instances_ASD_counts_"+appname+"_cutoff_seconds_"+str(cutoff)+".png"
    plt.savefig(savepath)#,bbox_inches='tight')
    plt.close()
    return x1

#http://stackoverflow.com/questions/17907614/finding-local-maxima-of-xy-data-point-graph-with-numpy
def local_maxima(xval, yval):
    xval = np.asarray(xval)
    yval = np.asarray(yval)

    sort_idx = np.argsort(xval)
    yval = yval[sort_idx]
    gradient = np.diff(yval)
    maxima = np.diff((gradient > 0).view(np.int8))
    return np.concatenate((([0],) if gradient[0] < 0 else ()) +
                          (np.where(maxima == -1)[0] + 1,) +
                          (([len(yval)-1],) if gradient[-1] > 0 else ()))
                     

#A D S T
def all_calls():
    names=['android_skout_new_logic_ekta_1504','dream_league_soccer_new_logic_ekta_2_1504','social_word_game_new_logic_ekta_1504_updated','truecaller_caller_id_and_block_new_logic_ekta_1504']
    x_peaks=[]
    for name in names :
        filehandle1='/home/ekta/Desktop/BACKUP/DynamicBidding/latestData/latestData/ARI/Newdata1504/time_diff_analysis/Finding_Peaks/folder2/'+name+'.tsv'
        filehandle2='/home/ekta/Desktop/BACKUP/DynamicBidding/latestData/latestData/ARI/Newdata1504/time_diff_analysis/Finding_Peaks/folder2/'+name+'_CSV.csv'
        #tsv_to_csv(filehandle1, filehandle2) # converting to csv , only once
        cutoff=[2*60,30]
        """
        pool = ThreadPool(4)
        # Open the urls in their own threads
        # and return the results    
        results = pool.map(urllib2.urlopen, urls)  #actual map on your custom function happens here
        #close the pool and wait for the work to finish
        pool.close()
        pool.join()
        """

        x1=other_processing(filehandle2,name,cutoff[0])
        x2=other_processing(filehandle2,name,cutoff[1])
        x_peaks.append(x1)
        #y_optim.append(y1)
        #print 'processing over for %s' %name.split('_new_logic')[0]
    return x_peaks # x_optim has all the peaks across all the apps in # ADST order

# for these x peaks in x_peaks, print the percentage coverage
