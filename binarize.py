#!/usr/bin/env python2.6
#Mami Sasaki
#Nat Byington
#hw2:Q2 binarizes features

#import libraries
import sys,re

#open files
input = open(sys.argv[1],'r')
output = open(sys.argv[2],'w')
data = input.read()
sentences = data.split('\n')

# change the value to binary
for s in sentences: 
   if not s:break
   news = re.sub(' [1-9]+[0-9]*([\s\n]*)',' 1\g<1>',s)
   output.write("%s\n" % news)

input.close()
output.close()
