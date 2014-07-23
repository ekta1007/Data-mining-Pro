#Author : Ekta Grover,08/04/2014
# Window specific Average session time

#from __future__ import division
from pylab import *
import pandas  as pd , csv
import matplotlib.pyplot as plt
from matplotlib import rc
from itertools import chain 
import random
import numpy as np
from itertools import chain #list(chain.from_iterable(x)
from itertools import izip, islice
import operator
#placing anchored text within the figure
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
rc('mathtext', default='regular')
import pickle # to dump objects in a text file


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


def create_dict(filehandle2):
    #num_lines, filehandle2=tsv_to_csv(filehandle1, filehandle2) # only for the first time round
    df = pd.read_csv(filehandle2,skiprows=0, sep=',')
    print "done"
    p=list(set(df['user']))
    len(p)
    d_ARI={}
    d_ARI_diff={}
    for key in p[0:500]:
        d_ARI[key]=sorted(list(df[df['user']==key]['etime']))
        the_list=d_ARI[key]
        temp=[]
        for  next_item,current_item in izip(islice(the_list, 1, None),the_list):
            temp.append(next_item-current_item)
        d_ARI_diff[key]=temp

    # write this dict to a file
    input_dump_d_ARI="C:/Users/Ekta.Grover/Desktop/Dynamic Bidding/latest data/latest data/ARI/d_ARI_poc_8April.txt"
    input_dump_d_ARI_diff="C:/Users/Ekta.Grover/Desktop/Dynamic Bidding/latest data/latest data/ARI/d_ARI_diff_poc_8April.txt"
    with open(input_dump_d_ARI, 'wb') as handle:
      pickle.dump(d_ARI, handle)
    with open(input_dump_d_ARI_diff, 'wb') as handle:
      pickle.dump(d_ARI_diff, handle)
    
    return d_ARI_diff

def calculate_ARI_window(d_ARI_diff,window):
    sum_tot,n = 0,0
    for key in d_ARI_diff :
        for temp in d_ARI_diff[key]:
            if temp <= window:  
                sum_tot=sum_tot+temp
                n=n+1
    avg=float(sum_tot)/float(n)
    return avg

def plot_ARI(d_ARI_diff,window,avg,time_metric):
    keys=d_ARI_diff.keys()
    map_back={}
    colors = cm.rainbow(np.linspace(0, 1, len(keys)))
    i=1
    for key in keys:
        map_back[i]=key
        i=i+1
    # plot each point with u1, u2 etc... wrt all diff points against time
    labels=['u'+str(i) for i in range(1,len(keys)+1)]
    fig, ax = plt.subplots()
    for i in range(1,len(keys)):
        for m in range(0,len(d_ARI_diff[map_back[i]])):
            for item in d_ARI_diff[map_back[i]] :
                if item<=window:
                    rects1=ax.scatter(i, item, color=colors[i])
     xlim([1,len(labels)+1])
    plt.xticks(np.arange(1, len(labels)+1),rotation=10, rotation_mode="anchor")
    if time_metric=='minutes':
        window=window/60
        avg=float(avg)/float(60)
        ylim([1,window])
    else :
        ylim([1,window])
    #The Average ASL should ideally be calculated over the entire data-set, but the plots are over a subset of data(for friendlier visualization)
    title='\n Average session length(ASL) for users across different time windows \n Window = '+str(window)+' '+str(time_metric)
    plt.suptitle(title, fontsize=12)
    plt.ylabel('Session length for different request for bids at a specific app \n(in '+str(time_metric)+' )')
    plt.xlabel('User id')
    # plot this average along with other stuff - distribution of time to click
    at = AnchoredText("Average :"+str(avg)+' '+str(time_metric)+" in Window size : "+str(window)+' ' +time_metric,prop=dict(size=10), frameon=True,loc=2,)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)
    # save plots
    savepath="C:/Users/Ekta.Grover/Desktop/Dynamic Bidding/latest data/latest data/ARI/ASL_"+str(window)+ "_" +time_metric.upper()+".png"
    plt.savefig(savepath,bbox_inches='tight')
    plt.close() 
    #plt.show()


# now execute this whole script against 30 seconds, 1 min, 30 min,60 minutes
filehandle1="C:/Users/Ekta.Grover/Desktop/Dynamic Bidding/latest data/latest data/ARI/ios_skout_new_multiple_COMPLETE.tsv"
filehandle2="C:/Users/Ekta.Grover/Desktop/Dynamic Bidding/latest data/latest data/ARI/ios_skout_new_multiple_COMPLETE_CSV.csv"
i=0
d_ARI_diff=create_dict(filehandle2)
for window in [30,60,30*60,60*60]:
    time_metric=['seconds','seconds', 'minutes','minutes']
    avg=calculate_ARI_window(d_ARI_diff,window)
    plot_ARI(d_ARI_diff,window,avg,time_metric[i])
    i=i+1



