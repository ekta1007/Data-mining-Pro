"""
Author : Ekta Grover, 19-03-2014
Min sample size constraints, confidence
Reference & Resources -:
http://resources.esri.com/help/9.3/arcgisdesktop/com/gp_toolref/spatial_statistics_toolbox/what_is_a_z_score_what_is_a_p_value.htm
http://www.abtester.com/calculator/
https://developer.amazon.com/sdk/ab-testing/reference/ab-math.html

Usage : takes a list of list, one each for a target group , of the format as below, and outputs 
Conversion Rate Z-Score Confidence Sample-Size Percentage Change Conversion Range
#perform=[[182,35],[180, 45],[189, 28],[188, 61]]
#perform = [[1064,320],[1043,250]]
"""


import math, sys
import ast
#perform=[[182,35],[180, 45],[189, 28],[188, 61]]
#perform = [[1064,320],[1043,250]]


perform =sys.argv[1]
perform=ast.literal_eval(perform)
def convert(perform):
    return float(perform[1])/float(perform[0])

""" Z score works on control group vis a vis each target group"""
def zscore (perform,m) : # m is the index of the target group
   z = convert(perform[m])-convert(perform[0]) # Difference in means
   s =(convert(perform[m])*(1-convert(perform[m])))/perform[m][0]+(convert(perform[0])*(1-convert(perform[0])))/perform[0][0]
   return float(z)/float(math.sqrt(s))
def format_number(number):
    return round(number, 3)
    
def cumnormdist(x) :
    b1 = 0.319381530
    b2 = -0.356563782
    b3 = 1.781477937
    b4 = -1.821255978
    b5 = 1.330274429
    p = 0.2316419
    c = 0.39894228
    h=math.exp(-x * x / 2.0)
    if(x >= 0.0) :
        t = 1.0 / ( 1.0 + p * x )
        return (1.0 - c * h * t *( t *( t * ( t * ( t * b5 + b4 ) + b3 ) + b2 ) + b1 ))
    else :
        t = 1.0 / ( 1.0 - p * x );
        return ( c * h * t *( t *( t * ( t * ( t * b5 + b4 ) + b3 ) + b2 ) + b1 ))
   
def ssize(conv):
    a = 3.84145882689
    bs = [0.0625, 0.0225, 0.0025]
    res=[]
    for b in bs:
	if conv==0:
		res.append(0)
	else:
        	res.append((int) ((1-conv)*a/(b*conv)))
    return res

def conversion_range(conv,perform,m):
   try:
   	s=math.sqrt((conv*(1-conv))/perform[m][0])
   	return format_number((conv+(1.65*s))*100), format_number((conv-(1.65*s))*100)
   	#return (conv+(1.65*s))*100, (conv-(1.65*s))*100
   except: return 0
	
#(1-cumnormdist(zscore(perform,1)))*100
def changepercent(perform,m) : # will always compare against control group # (Target - CG)/CG
   	try:
		return ((convert(perform[m])-convert(perform[0]))*100/convert(perform[0]))
	except:
		return 0
# Calling the performance benchmarks
str1 = "%s %s %s %s %s %s" %("Conversion Rate","Z-Score".rjust(15),"Confidence".rjust(13),"Sample-Size".rjust(10),"Percentage Change" , "Conversion Range" )

OutputFileHandle='/usr/share/apache-tomcat-7.0.52/webapps/report_py.txt'
with open(OutputFileHandle,'w') as outputFile:
	for i in range(0,len(perform)):
		if i ==0 : # target group 0 , z score & confidence is not applicable
    			str2 = "%s|%s|%s|%s"%((str(format_number(convert(perform[i])*100))+str('%')),str(ssize(convert(perform[i]))).rjust(40),str(format_number(changepercent(perform,i))),str(conversion_range(convert(perform[i]),perform,i)))
        		outputFile.write(str(str2)+"\n")
    		elif i >0:
    			str3 = "%s|%s|%s|%s|%s|%s" %((str(format_number(convert(perform[i])*100))+str('%'), format_number(zscore(perform,i)),str(format_number(cumnormdist(zscore(perform,i))*100)), ssize(convert(perform[i])),format_number(changepercent(perform,i)),conversion_range(convert(perform[i]),perform,i)))
			outputFile.write(str(str3)+"\n")
outputFile.close()

"""
Output -:
Conversion Rate Z-Score Confidence Sample-Size Percentage Change Conversion Range
30.0751879699% [142, 396, 3572] 0.0 (32.39489404149127, 27.755481898358347)
23.9693192713% -3.1641397476 0.0777776243205% [194, 541, 4874] -0.203020134228 (26.150361526280026, 21.788277016385365)
"""

