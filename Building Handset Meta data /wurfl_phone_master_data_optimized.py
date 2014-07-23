import re , nltk
from nltk.tokenize import RegexpTokenizer
#import tokenize
from itertools import chain
from nltk import bigrams, trigrams
import math, string
import urllib2, urllib
import csv
import operator
import pandas as pd
from user_agents import parse
from urllib import urlencode
# pick from here
#http://stackoverflow.com/questions/10751127/returning-multiple-values-from-pandas-apply-on-a-dataframe
#http://stackoverflow.com/questions/16236684/apply-pandas-function-which-returns-multiple-values
# http://stackoverflow.com/questions/12329853/how-to-rearrange-pandas-column-sequence
"""
    is_tablet: false
    pointing_method: stylus
    the_file=open(txt_path, 'w')
the_file.write('raw_user_agent|user_agent.browser.family|user_agent.browser.version_string|user_agent.os.family|user_agent.os.version_string|user_agent.device.family\n')
for i in range(0,len(df)) :
    ua_string=df['ua'].values[i]
    user_agent = parse(ua_string)
    try :
        the_file.write(str(ua_string)+'|'+str(user_agent.browser.family)+'|'+str(user_agent.browser.version_string)+'|'+str(user_agent.os.family)+'|'+str(user_agent.os.version_string)+'|'+str(user_agent.device.family+'\n'))
    except :
        the_file.write(ua_string.encode('utf-8')+'|'+user_agent.browser.family.encode('utf-8')+'|'+user_agent.browser.version_string.encode('utf-8')+'|'+user_agent.os.family.encode('utf-8')+'|'+user_agent.os.version_string.encode('utf-8')+'|'+user_agent.device.family.encode('utf-8')+'\n')
        #ua_string.encode('utf-8')
print "done writing the csv for ua"
the_file.close()


"""

def ua_master_data(x):
    #print "OK"
    #print x
    try :
        ua_string=x
    except UnicodeEncodeError:
        print x
        ua_string=x.encode('utf-8')
        x=x.encode('utf-8')
    except Exception, e:
        print e.__doc__
        print e.message
    user_agent = parse(ua_string)
    query_args = {'user-agent-string':x.encode('utf-8')+'' }
    try :
        encoded_args = urllib.urlencode(query_args)
        url = 'http://tools.scientiamobile.com/?' + encoded_args
        html = urllib.urlopen(url).read()
        raw = nltk.clean_html(html)
        raw=str(raw)
        #TypeError: expected a character buffer object
        #print raw, type(raw)
    except UnicodeEncodeError:
        print x # print the problematic values - ideally should store this in a file
        pass
    try:
        if (raw.find("identified as a")!=-1) or raw.find("resolution_width:"!=-1):
            i_begin=raw.find("identified as a")
            i_end=raw.find("Link to this result")
            try :
                name=raw[i_begin+len("identified as a"):i_end].strip().encode('utf-8')
            except Exception, e:
                name=raw[i_begin+len("identified as a"):i_end].strip()
                name=name.decode('utf-8')
                name=name.encode('utf-8')
                print e.__doc__
                print e.message
            try :
                i_begin=raw.find("is_tablet:")
                i_end=raw.find("resolution_width:")
                tablet_pointing_method=raw[i_begin+len("is_tablet:"):i_end].strip()
                is_tablet=tablet_pointing_method.replace("pointing_method:" ,"").strip().split(" ")[0]
            except Exception, e:
                print name
                print e.__doc__
                print e.message
            try :
                i_begin=raw.find("pointing_method:")
                i_end=raw.find('resolution_width:')
                pointing_method=raw[i_begin+len('pointing_method:'):i_end].strip()
                #pointing_method=tablet_pointing_method.replace("pointing_method:" ,"").strip().split(" ")[1]
            except IndexError:
                pointing_method =''
            try :
                index_begin=raw.find("resolution_width:")
                index_end=raw.find("This is just a partial list of capabilities.")
                width=raw[index_begin:index_end].replace("resolution_width:","").replace("resolution_height:","").strip().split(" ")[0]
                height=raw[index_begin:index_end].replace("resolution_width:","").replace("resolution_height:","").strip().split(" ")[2]
            except IndexError:
                width=''
                height=''
                #print str(x), url,name,is_tablet,pointing_method,width,height
            try :
                user_agent_masterclass=name.split()[0].lower()
            except Exception, e:
                user_agent_masterclass='Not Available'
                print e.__doc__
                print e.message
        #print x.encode('utf-8'), url,name,is_tablet.encode('utf-8'),pointing_method.encode('utf-8'),width,height,user_agent.browser.family.encode('utf-8'),user_agent.browser.version_string.encode('utf-8'),user_agent.os.family.encode('utf-8'),user_agent.os.version_string.encode('utf-8'),user_agent.device.family.encode('utf-8'),user_agent_masterclass
        return pd.Series({'A': x.encode('utf-8'), 'B': url.encode('utf-8'),'C': name,'D': is_tablet.encode('utf-8'),'E': pointing_method.encode('utf-8'), 'F': width,'G': height,'H': user_agent.browser.family.encode('utf-8'),'I': user_agent.browser.version_string.encode('utf-8'),'J': user_agent.os.family.encode('utf-8'),'K': user_agent.os.version_string.encode('utf-8'),'L': user_agent.device.family.encode('utf-8'),'M': user_agent_masterclass})
    except Exception, e:
        return pd.Series({'A': x.encode('utf-8'), 'B': url.encode('utf-8'),'C': 'Not Available','D': 'Not Available','E': 'Not Available', 'F': width,'G': height,'H': user_agent.browser.family.encode('utf-8'),'I': user_agent.browser.version_string.encode('utf-8'),'J': user_agent.os.family.encode('utf-8'),'K': user_agent.os.version_string.encode('utf-8'),'L': user_agent.device.family.encode('utf-8'),'M': user_agent_masterclass})
        print e.__doc__
        print e.message
        pass
 

"""
except Exception, e:
    print e.__doc__
            print e.message
"""
    #pd.Series({'user_agent':  x.encode('utf-8'), 'url': url,'name':name.encode('utf-8') , 'is_tablet': is_tablet.encode('utf-8'), 'pointing_method': pointing_method.encode('utf-8'),'width': width, 'height': height,  'user_agent.browser.family': user_agent.browser.family.encode('utf-8'),'user_agent.browser.version_string': user_agent.browser.version_string.encode('utf-8'),'user_agent.os.family': user_agent.os.family.encode('utf-8'),
#'user_agent.os.version_string': user_agent.os.version_string.encode('utf-8'),'user_agent.device.family': user_agent.device.family.encode('utf-8'),'user_agent.masterclass': user_agent_masterclass})
    #x.encode('utf-8'), url,name.encode('utf-8'),is_tablet.encode('utf-8'),pointing_method.encode('utf-8'),width,height,user_agent.browser.family.encode('utf-8'),user_agent.browser.version_string.encode('utf-8'),user_agent.os.family.encode('utf-8'),user_agent.os.version_string.encode('utf-8'),user_agent.device.family.encode('utf-8'),user_agent_masterclass

#df['ua'].apply(lambda x : time_day_funct(x))

filehandle ="/home/ekta/Desktop/LR_Adnear/DATANEW/ua_click_splits/ua_click_uniqueaa"
df= pd.read_csv(filehandle,encoding='utf-8',sep='|',skiprows=0)#nrows=3,names=['ua'],skiprows=321)
#df= pd.read_csv(filehandle,encoding='utf-8',sep='|',nrows=3,names=['ua'],skiprows=321)#,nrows=2)#,nrows=1)#,nrows=1000)#,skiprows=1000)
txt_path='/home/ekta/Desktop/LR_Adnear/DATANEW/PART_5_ua_click_uniqueaa.txt'
#PART_4_wurfl_resolution_width_fetched_from_ScientiaMobile_cloud_complete_file.txt'
#PART_2_wurfl_resolution_width_fetched_from_ScientiaMobile_cloud_complete_file.txt'

#df['A'],df['B'],df['C'], df['D'],df['E'],df['F'],df['G'],df['H'],df['I'],df['J'],df['K'],df['L'],df['M']
v=df['ua'].apply(lambda x : ua_master_data(x))
#the_file=open(txt_path, 'w')
#df=df.drop('ua',axis=1)
# write the dataframe to csv
file_name=txt_path
print "started writing to file"
v.to_csv(file_name, sep='|', encoding='utf-8',index=False)
print "finished writing the file"

"""
the_file.write('user_agent|url|name|is_tablet|pointing_method|width|height|user_agent.browser.family|user_agent.browser.version_string|user_agent.os.family|user_agent.os.version_string|user_agent.device.family|user_agent.masterclass\n')
        try :
            the_file.write(str(df['ua'].values[i])+'|'+ url+'|'+name+'|'+is_tablet+'|'+pointing_method+'|'+width+'|'+height+'|'+str(user_agent.browser.family)+'|'+str(user_agent.browser.version_string)+'|'+str(user_agent.os.family)+'|'+str(user_agent.os.version_string)+'|'+str(user_agent.device.family)+'|'+str(user_agent_masterclass)+'\n')
        except UnicodeEncodeError:
            the_file.write(df['ua'].values[i].encode('utf-8')+'|'+ url+'|'+name.encode('utf-8')+'|'+is_tablet.encode('utf-8')+'|'+pointing_method.encode('utf-8')+'|'+width+'|'+height+'|'+user_agent.browser.family.encode('utf-8')+'|'+user_agent.browser.version_string.encode('utf-8')+'|'+user_agent.os.family.encode('utf-8')+'|'+user_agent.os.version_string.encode('utf-8')+'|'+user_agent.device.family.encode('utf-8')+'|'+user_agent_masterclass+'\n')
    the_file.close()
"""   
#for i in range(0,len(df)):
    
#print "finished writing the file"
