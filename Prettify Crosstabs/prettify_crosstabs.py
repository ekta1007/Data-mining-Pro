# Author : Ekta Grover, 28-04-2014
#Prettify_crosstabs - this file can do pretty crosstabs for any attribute of a DataFrame - ie. with mutiple classes against an attribute

from __future__ import division
from pylab import *
import pandas  as pd , csv
import matplotlib.pyplot as plt
from matplotlib import rc
import random
import numpy as np
from itertools import chain #list(chain.from_iterable(x))
import operator, codecs,time
#placing anchored text within the figure
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
rc('mathtext', default='regular')


# Algorithm : First Prepare data Consumable to get Crosstabs per variable
# Cross tabs have to be passed on ENTIRE data - not the sampled one
"""
population_coverage calculates the % population per category of Column name/Attribute
ctr_rates get the Success rates per variable independent of it's percentage population

#Inputs : df, var 
#var= pick recursively from df.columns 
Other options :
# showing labels only if the CTR is greater than base CTR, by some,std dev say
# showing labels if the CTR is far lesser, so we can prune this
#Get the colnames for plotting agianst app categories
"""


def ctr_rates(df,var):
    myfunc1 = lambda x: 1 if (x == 'click') else 0
    df['click'] = df['event_adlogs'].apply(myfunc1)
    df['impression'] = 1
    f=df.pivot_table(rows=var, aggfunc=[len,np.sum])
    #CTR rates
    base_ctr=(float(sum(df['click']))*100)/sum(df['impression'])
    ctr_var=dict(f['sum']['click']*100/f['sum']['impression'])
    return base_ctr,ctr_var 


# 1st find the variable attributes that have atleast n% coverage, and for these show the CTR's
def show_prospects_by_population_coverage(df,var,n):
    perct_freq=dict((df[var].value_counts()*float(100))/len(df[var]))
    pop_coverage={}
    for key,value in perct_freq.items():
        if value>=n :
            pop_coverage[key]=value #.append([key,value])
    return pop_coverage #can get the keys for pop_coverage by population coverage criteria 


  
def show_prospects_by_CTR(df,var,keys): # keys=pop_coverage.keys() fetched from show_prospects_by_population_coverage(df,var,n)
    base_ctr,ctr_var = ctr_rates(df,var)
    prospects={}
    # Display CTR for all prospects 
    for key in keys :
        prospects[key]=ctr_var[key] 
    return base_ctr, prospects

#now just create the combined vector for all these prospects
#show_performance has the var name, it's CTR &its percentage coverage in pop - this is the data used in cross tab per "var" name, per value across the rows
def show_all(df,var,n,prospects,base_ctr): #,pop_coverage
    if prospects !=None and base_ctr != None :
        flag =1 #If flag=1, plotting only prospects
        show_performance=[]
        keys= prospects.keys()
        pop_coverage=show_prospects_by_population_coverage(df,var,n)
        for items in keys :
            temp=[items,prospects[items],pop_coverage[items]]
            show_performance.append(temp)
    elif prospects != None and base_ctr == None : # prospecting by 1% coverage
        show_performance=[]
        flag =0 # setting a flag to indicate if we will be plotting all, or just prospects. 
        base_ctr,ctr_var=ctr_rates(df,var) # everything !
        perct_freq=dict((df[var].value_counts()*float(100))/len(df[var]))
        keys=ctr_var.keys()
        for items in ctr_var.keys() :
            temp=[items,ctr_var[items],perct_freq[items]]
            show_performance.append(temp)
    elif prospects ==None and base_ctr == None :
        show_performance=[]
        flag =0 # setting a flag to indicate if we will be plotting all, or just prospects. 
        base_ctr,ctr_var=ctr_rates(df,var) # everything !
        perct_freq=dict((df[var].value_counts()*float(100))/len(df[var]))
        keys=ctr_var.keys()
        for items in ctr_var.keys() :
            temp=[items,ctr_var[items],perct_freq[items]]
            show_performance.append(temp)
    #print show_performance,flag
    return base_ctr,show_performance,flag


# All functions for plotting
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.itervalues():
        sp.set_visible(False)

def autolabel(rects,ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),ha='center', va='bottom')


def autolabel_custom(rects,label,ax):
    # Custom display the labels wither where pop >n% , or CTR rate is significant
    # attach some text labels
    i=0
    for rect in rects:
        if label[i] !='':
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),ha='center', va='bottom')
        else :
            pass
        i=i+1

def pretty_plots(n,var,show_performance,base_ctr,flag) :
    xx=show_performance
    m=[]
    labels=[x[0] for x in xx]
    print "labels in pretty plots"
    print labels
    try :
        labels=[y.encode('utf-8') for y in labels] #y.decode('utf-8').encode('utf-8')
    except AttributeError:
        pass
        #labels=[y for y in labels]
    print labels
    #print "printing labels"
    #print [label for label in labels]
    #print labels, len(xx)
    #print "labels done"
    ctr_rate=[x[1] for x in xx]
    pop_coverage=[x[2] for x in xx]
    label=[]
    pop_coverages=[]
    ctr_rates=[]
    if flag ==0 : # if "0", we will plot everything
        for i in range(0,len(labels)):
            if ctr_rate[i]>base_ctr :
                label.append(labels[i]) # append that label
                pop_coverages.append(pop_coverage[i])
                ctr_rates.append(ctr_rate[i])
            elif  pop_coverage[i] >=n :
                label.append(labels[i])
                pop_coverages.append(pop_coverage[i])
                ctr_rates.append(ctr_rate[i])
    elif flag ==1 : #If flag=1, plotting only prospects
        label=labels
        pop_coverages=pop_coverage
        ctr_rates=ctr_rate
    N = len(label) #N = Total # of unique values in df[var]
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35
    #alphab=label
    fig, ax = plt.subplots()
    par1 = ax.twinx()
    make_patch_spines_invisible(par1)
    rects1 = ax.bar(ind, pop_coverages, width, color='b')
    lines_1=par1.plot(ind + 0.5*width, ctr_rates,linestyle='', marker='*', markerfacecolor ='g', markeredgewidth='1')
    #Plot a straight line to represent the CTR
    plt.axhline(y=base_ctr, xmin=0, xmax=1,color='c') 
    ax.set_xlabel(var,style='italic',size=20)
    ax.set_ylabel("Population coverage(in %)",style='italic',size='large')
    par1.set_ylabel("CTR rates",style='italic',size='large')
    ax.set_title('Cross-tabs with percentage population against it\'s CTR rates for %s categories'%var,style='italic')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(label, rotation=10, rotation_mode="anchor") #rotation='vertical')
    #placing anchored text within the figure, as supplementary legend
    at = AnchoredText("The horizontal line is Base CTR rate",prop=dict(size=10), frameon=True,loc=2,)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)
    autolabel_custom(rects1,label,ax)
    ax.legend((rects1[0],lines_1[0]), ('% Population coverage', 'CTR rate'),prop=dict(size=10), numpoints=1 )
    plt.legend()
    plt.legend(numpoints=1)
    #plt.show()
    savepath='/home/ekta/Desktop/BACKUP/DynamicBidding/latestData/'+str(var)+ "_" + str(flag)+".png"
    #"C:/Users/Vikas Singhai/Desktop/Dynamic Bidding/latest data/"+str(var)+ "_" + str(flag)+".png"
    plt.savefig(savepath,bbox_inches='tight')



def init(df,n,var,features):
    # Without propecting - flag =0 
    base_ctr,show_performance,flag =show_all(df,var,n,prospects=None,base_ctr=None)
    pretty_plots(n,var,show_performance,base_ctr,flag)
    # Next plot only prospects, flag =1
    pop_coverage=show_prospects_by_population_coverage(df,var,n)
    base_ctr, prospects=show_prospects_by_CTR(df,var,pop_coverage.keys())
    base_ctr,show_performance,flag=show_all(df,var,n,prospects=prospects,base_ctr=base_ctr)
    pretty_plots(n,var,show_performance,base_ctr,flag)
    keys=[x[0] for x in show_performance] # only significant keys /ie. prospects per variable
    try :
        features[var]=[var+"_"+key.encode('utf8') for key in keys] # initially was features[var]=keys
    except AttributeError or TypeError: 
        features[var]=[str(var)+"_"+str(key) for key in keys]
    print "inside of init"
    print var, features[var]
    return features

def time_day_funct(x,y):
    time_day=[]
    if isinstance(x, basestring) :
        return x.replace(y,'').strip().split(':')[0]
    elif isinstance(x, int) :
        return append(0)
    elif isinstance(x,float):
        return x

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def define_category(iab_list):
    cat_list_iab=[]
    cat_list_string=[]
    for k in range(0, len(iab_list)):
        if  isinstance(iab_list[k],basestring) :
            x=iab_list[k].split(',')
            for i in x :
                if hasNumbers(i) is True and i!= ''  :
                    cat_list_iab.append(i)
                elif i!= '' :
                    cat_list_string.append(i)
        elif isinstance(iab_list[k],float) :
            pass
    return list(set(cat_list_iab)), list(set(cat_list_string))

def boolean(df_appcat,cat_list_iab):
    m=[]
    for i in range(0,len(df_appcat)):
        h=','+ cat_list_iab +','
        if  isinstance(df_appcat[i],basestring) and df_appcat[i].find(h)!=-1:
            m.append(1)
        elif isinstance(df_appcat[i],float) or df_appcat[i].find(h)==-1:
            m.append(0)
    index=range(0,len(m))
    s = pd.Series(m, index=index)
    return s

# this will return the new dataframe with cols
def mapping(df):
    col_names=define_category(df['appcat'])
    for col_name in col_names :
        df[col_name]=boolean(df["appcat"],col_name)
    return col_names,df

#dummify only those features that are significant & drop the others
def dummify_features(df,features,var):  #features has the sublist, get_dummies does everything
    key=var
    try :
        df[key]=[val.encode("utf-8")if isinstance(val,float)==False else  'Not_Available' for val in df[key]]
    except AttributeError or TypeError:
        df[key]=[str(val) if isinstance(val,float)==False else  'Not_Available' for val in df[key]]
    dummies = pd.get_dummies(df[key], prefix=key) # will have all dummified
    x=list(dummies.columns)
    atom_col = [c for c in dummies.columns if c in features[key]] # we should append only the cols in atom_col to orignal df
    temp_df=dummies[atom_col]
    df=pd.concat([df, temp_df], axis=1)
    return df
   

# Main function
def main_prettify():
    filehandle='/home/ekta/Desktop/BACKUP/DynamicBidding/latestData/12_22_mopub_winlogs_adlogs_requests_day_week_data_joined_COMPLETE_CSV.csv'
    n=5 # At least 5% coverage, or CTR> base CTR # can use Input here
    df= pd.read_csv(filehandle,skiprows=0, encoding='utf-8',sep=',',nrows=100)
    col_names,df=mapping(df)
    features={}
    var1,var2='date_full','date_custom'
    time_day=df.apply(lambda x : time_day_funct(x[var1],x[var2]), axis=1)
    time_day=pd.DataFrame(time_day)
    time_day.columns = ['time_day']
    df=df.join(time_day)
    #var feeds from df.columns
    col_list=['time_day','appname','pubname','os','city', 'country', 'region'] # add MORE vars here
    print "printing col_list"
    print col_list
    for var in col_list :
        features[var]='' # initlialized dist of features
        features=init(df,n,var,features=features)
        df=dummify_features(df,features,var)
    return df,features,col_list

#Finally drop the cols in var that do not potentially impact CTR
df,features,col_list=main_prettify()
df=df.drop(col_list,axis=1)
# from this select cols to drop
"""
pd.get_dummies(df['devicemodel'],prefix='devicemodel')

"""
## usage in the main file : Take this feature vector for each var in df.columns and pass it along for the feature analysis
#n=5
#df,features,col_list= main_prettify()
#df=df.drop(col_list,axis=1)
# post picking up the dummified cols from here( On FULL DATA)- push the features on sample data


