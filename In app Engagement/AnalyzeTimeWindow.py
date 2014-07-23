# Analyze time
# Author : Ekta Grover, 04/01/2014

from __future__ import division
import numpy
from pylab import *
import pandas  as pd , csv
import matplotlib.pyplot as plt


filehandle1="C:/Users/Ekta.Grover/Desktop/analyze.tsv"
df = pd.read_csv(filehandle1,skiprows=0, sep=',')
my_dict={}
cutoff=3600 # 1 hour 
#cutoff=43200 # 12 hours
#cutoff=604800 # 7 day
#cutoff=9999999999 # All data days
df1=df[df['diff']>=0][['diff']]
df2=df1[df1['diff']<=cutoff][['diff']]/(60) # Modify this to refect the base window(x axis - in minutes(60), hours(60*60), days(60*60*24))
#for i in range(0,len(df)):
  #   if df['diff'].ix[i] >=0 :
for key in df2['diff']  :
     my_dict[key] =''
for key in df2['diff'] :
     if my_dict[key] =='' :
          my_dict[key]=1
     else :
          my_dict[key]=my_dict[key]+1

# Plot the individual keys against its counter
x=[key for key in my_dict.keys()]
y=[log(imp) for imp in my_dict.values()]
#label=[]
#fig = plt.figure()
xlim([min(x),max(x)])
ylim([min(y),max(y)])
#plt.xticks(np.arange(min(x), max(x)+1, 24)) # Set x tickers based on your custom criteria
plt.suptitle('How long after the impressions do the users click? \n The scale is taken as a log scale since literature suggests like-wise \n Window =  One hour', fontsize=12)
plt.ylabel('# Log Clicks \n To get back the actual clicks do exp(#click)')
plt.xlabel('Difference of time between clicks & impressions : in minutes')
plt.scatter(x,y)
plt.show()

#cutoff_custom is in seconds
def percent_area(df1,cutoff_custom):
     df2=df1[df1['diff']<=cutoff_custom][['diff']]
     percent=float(len(df2))/float(len(df1))*100
     return percent

# To test the percentage coverage for 12 hours
cutoff_custom=60*60*12
percent_area(df1,cutoff_custom)
