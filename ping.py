from os import popen
from string import split, join
from re import match
import subprocess
import os

   # execute the code and pipe the result to a string

rtr_table = [elem.strip().split() for elem in popen("route print").read().split("Metric\n")[1].split("\n") if match("^[0-9]", elem.strip())]

#print "Active default gateway:", rtr_table[0][2]
x=rtr_table[0][2]
#x has a.a.a.a 
y = x[:x.rfind(".")]
# y has a.a.a
# in order to test in range of 1 to 255 for the default gateway
for i in range(1,255):
#ping by sending 1 packet and wait for 500 milli seconds 
test = "ping -n 1 -w 500 %s.%d" % (y,i)
process = subprocess.Popen(test, shell=True, stdout=subprocess.PIPE)
   # give it time to respond
process.wait()
   # optional check (0 --> success)
   #print process.returncode
   # read the result to a string
result_str = process.stdout.read()
   # test it ...
   # print result_str
#from arp we get mac address and corresponding ip address and state as we use '-a'
lines=os.popen('arp -a')
for line in lines:
   print line
