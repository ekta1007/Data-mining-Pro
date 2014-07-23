"""
Author : Ekta Grover
Usage : Given a raw user agent, processes it to extract the following fields to build handset Metadata
user_agent|url|name|is_tablet|pointing_method|width|height|user_agent.browser.family|user_agent.browser.version_string|user_agent.os.family|user_agent.os.version_string|user_agent.device.family|user_agent.masterclass
"""
import re , nltk
from itertools import chain
import math, string
import urllib2, urllib
import csv
import operator
import pandas as pd
from user_agents import parse
from urllib import urlencode

filehandle ="/home/ekta/ua_to_process"
df= pd.read_csv(filehandle,skiprows=0, encoding='utf-8',sep='|')
txt_path='/home/ekta/ua_processed'
the_file=open(txt_path, 'w')
the_file.write('user_agent|url|name|is_tablet|pointing_method|width|height|user_agent.browser.family|user_agent.browser.version_string|user_agent.os.family|user_agent.os.version_string|user_agent.device.family|user_agent.masterclass\n')
for i in range(0,len(df)):
    try :
        ua_string=df['ua'].values[i]
    except UnicodeEncodeError:
        ua_string=df['ua'].values[i].encode('utf-8')
        df['ua'].values[i]=df['ua'].values[i].encode('utf-8')
    user_agent = parse(ua_string)
    query_args = {'user-agent-string':df['ua'].values[i].encode('utf-8')+'' }
    #since we are parsing raw html(text), we need to do a try, catch, once for each attribute
    try :
        encoded_args = urllib.urlencode(query_args)
        url = 'http://tools.scientiamobile.com/?' + encoded_args
        html = urllib.urlopen(url).read()
        raw = nltk.clean_html(html)
    except UnicodeEncodeError:
        print i, df['ua'].values[i] # Print the problematic values - ideally should store this in a file
        pass
    if (raw.find("identified as a")!=-1) or raw.find("resolution_width:"!=-1):
        i_begin=raw.find("identified as a")
        i_end=raw.find("Link to this result")
        name=raw[i_begin+len("identified as a"):i_end].strip()
        if len(name)>0:
            name=" ".join(name.split()) # to replace multiple spaces with a single space
        i_begin=raw.find("is_tablet:")
        i_end=raw.find("resolution_width:")
        tablet_pointing_method=raw[i_begin+len("is_tablet:"):i_end].strip()
        is_tablet=tablet_pointing_method.replace("pointing_method:" ,"").strip().split(" ")[0]
        try :
            i_begin=raw.find("pointing_method:")
            i_end=raw.find('resolution_width:')
            pointing_method=raw[i_begin+len('pointing_method:'):i_end].strip()
        except IndexError:
            pointing_method =''
        index_begin=raw.find("resolution_width:")
        index_end=raw.find("This is just a partial list of capabilities.")
        try :
            width=raw[index_begin:index_end].replace("resolution_width:","").replace("resolution_height:","").strip().split(" ")[0]
            height=raw[index_begin:index_end].replace("resolution_width:","").replace("resolution_height:","").strip().split(" ")[2]
        except indexError:
            width=''
            height=''
        try :
            user_agent_masterclass=name.split()[0].encode('utf-8').lower()
        except IndexError:
            user_agent_masterclass='Not Available'
        try :
            the_file.write(str(df['ua'].values[i])+'|'+ url+'|'+name+'|'+is_tablet+'|'+pointing_method+'|'+width+'|'+height+'|'+str(user_agent.browser.family)+'|'+str(user_agent.browser.version_string)+'|'+str(user_agent.os.family)+'|'+str(user_agent.os.version_string)+'|'+str(user_agent.device.family)+'|'+str(user_agent_masterclass)+'\n')
        except UnicodeEncodeError:
            the_file.write(df['ua'].values[i].encode('utf-8')+'|'+ url+'|'+name.encode('utf-8')+'|'+is_tablet.encode('utf-8')+'|'+pointing_method.encode('utf-8')+'|'+width+'|'+height+'|'+user_agent.browser.family.encode('utf-8')+'|'+user_agent.browser.version_string.encode('utf-8')+'|'+user_agent.os.family.encode('utf-8')+'|'+user_agent.os.version_string.encode('utf-8')+'|'+user_agent.device.family.encode('utf-8')+'|'+user_agent_masterclass+'\n')
the_file.close()
print "finished writing the file"
