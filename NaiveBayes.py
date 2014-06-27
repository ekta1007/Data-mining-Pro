# Author : Ekta Grover, 27th june, 2014

from __future__ import division
import pandas as pd
import operator

order=['health','moderate','moderate','yes']
alternatives=['i100','i500']
# Naive bayes
"""
main interest is health
current exercise level is moderate
is moderately motivated
and is comfortable with technological devices
"""

filehandle="/home/ekta/Desktop/NB_example.csv"
df= pd.read_csv(filehandle,skiprows=0, encoding='utf-8',sep=',',index_col=False)#nrows=1000 #np.linalg.matrix_rank(A)
i=0
given={}
attributes=list(df.columns)
attributes.remove(df.columns[-1])  # we do this so that we don't take the model in the "given" attributes
for key in attributes:
    given[key]=order[i]
    i=i+1
prob_alternatives={}
for i in alternatives:
    prob_alternatives[i]=0
# Hypothesis to find maximum posterior probablity amongst the alternatives
prob={}
for m in alternatives:
    prob[m]={}
    for i in df[df.columns - [df.columns[-1]]]:
        prob[m][i]=0
        prob[m]['total']=len(df[df[df.columns[-1]]==m])

# Now start filling in the dict 
for key in prob.keys():
    for subkey in prob[key].keys() :
        if subkey is not 'total':
            prob[key][subkey]=len(df[(df[subkey]==given[subkey]) & (df[df.columns[-1]]==key)])
print prob

#To estimate 
prob_alternatives={}
m=1
h=prob[alternatives[0]].keys()
h.remove('total')
for key in prob.keys():
    m=prob[key]['total']/len(df)
    prob_alternatives[key]={}
    for subkey in h:
        m=m*prob[key][subkey]/prob[key]['total']
    prob_alternatives[key]=m
    print m
    m=1
print prob_alternatives
#MAP
print max(prob_alternatives.values())
Decision =max(prob_alternatives.iteritems(), key=operator.itemgetter(1))[0]
MapOfDecision=max(prob_alternatives.iteritems(), key=operator.itemgetter(1))[1]

                

#DATASET FOR THIS EXERCISE, adpated from Guide to DataMining

"""
Main Interest,Current Exercise Level,How Motivated,Comfortable with tech.Devices,Model
both,sedentary,moderate,yes,i100
both,sedentary,moderate,no,i100
health,sedentary,moderate,yes,i500
appearance,active,moderate,yes,i500
appearance,moderate,aggressive,yes,i500
appearance,moderate,aggressive,no,i100
health,moderate,aggressive,no,i500
both,active,moderate,yes,i100
both,moderate,aggressive,yes,i500
appearance,active,aggressive,yes,i500
both,active,aggressive,no,i500
health,active,moderate,no,i500
health,sedentary,aggressive,yes,i500
appearance,active,moderate,no,i100
health,sedentary,moderate,no,i100
"""
