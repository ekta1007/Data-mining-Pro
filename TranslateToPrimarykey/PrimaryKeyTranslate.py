#Author : Ekta Grover
# Usage : Translate string of userid to its Integer primary key representation 

#userid_mapper.py
#!/usr/bin/env python

import sys
for line in sys.stdin:
   line = line.strip()
   user_string, dat, appcat = line.split("\x7C")
   print "%s\t%s\t%s" % (user_string, dat, appcat)

#userid_reducer.py
#!/usr/bin/env python

from operator import itemgetter
import sys

current_user = None
counter = 0

for line in sys.stdin:
  line = line.strip()
  if len(line.split('\t')) ==3: 
    user_string, dat,appcat = line.split('\t')
 
    if current_user != user_string:
      counter += 1
   
    print "%d\t%s\t%s" %(counter, dat, appcat)
    current_user = user_string 

	
## To translate to primary keys ##
/usr/lib/hadoop/bin/hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.6.0.jar \
-D mapred.reduce.tasks=10 \
-file /root/ekta/userid_mapper.py -mapper /root/ekta/userid_mapper.py \
-file /root/ekta/userid_reducer.py -reducer /root/ekta/userid_reducer.py \
-input /user/hive/warehouse/app_analysis.db/InputTable\
-output /user/hive/warehouse/app_analysis.db/OutputTable