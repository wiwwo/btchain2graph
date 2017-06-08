#!/usr/bin/python

import logging


import requests, json, urllib2
import time, datetime
import gzip, sys, os, getopt
import random

latestBlockUrl="https://blockchain.info/latestblock"
rawBlockUrl="https://blockchain.info/rawblock/"

### response = urllib2.urlopen(latestBlockUrl)

# TODO - This sucks, but "Need for Speed"
### latestBlockAnswer = response.read()[15:81]

### if latestBlockAnswer[0]+latestBlockAnswer[65] != '""': exit

# TODO - DEBUG
#latestBlockAnswer = '"00000000000107925a52e24c838788a954d1a6d5858301c66d50b2a074787460"'
#latestBlockAnswer = '"00000000000304d51de00dc9c22b439030160b615303f0978d0e5ebc14c643b3"'
latestBlockAnswer = '"000000000002864e1165d5da2b9cf69512e96171f5d94c2ab1007c9a7933390b"'
response = urllib2.urlopen(rawBlockUrl+latestBlockAnswer[1:65])
rawBlockAnswer = response.read()

jsonBlockAnswer=json.loads(rawBlockAnswer)

print len(jsonBlockAnswer["tx"])
transNum=0

for transList in jsonBlockAnswer["tx"]:
  print 'TRANS HASH ->', transList["hash"]
  for transInput in transList["inputs"]:

    if transNum==0 :
      print 'mine'
      continue
    else:
      print 'IN ->',transInput["prev_out"]["addr"]

  for transOut in transList["out"]:

    print 'OUT ->',transOut["addr"]
    print 'VAL ->',transOut["value"]

  transNum=transNum+1
  print '--------------------'
print 'x'