#!/usr/bin/python

import logging


import requests, json, urllib2
import time, datetime
import gzip, sys, os, getopt
import random

DEBUG=1

sys.path.append( "myFunctions" )
sys.path.append( "classes" )

from myFunctions import *
from blockClass import *
from addrClass import *
from transactionClass import *

latestBlockHashAnswer = getLatestBlock()
if latestBlockHashAnswer[0]+latestBlockHashAnswer[65] != '""': exit

# TODO - DEBUG
#latestBlockHashAnswer = '"00000000000107925a52e24c838788a954d1a6d5858301c66d50b2a074787460"'
#latestBlockHashAnswer = '"00000000000304d51de00dc9c22b439030160b615303f0978d0e5ebc14c643b3"'
#latestBlockHashAnswer = '"000000000002864e1165d5da2b9cf69512e96171f5d94c2ab1007c9a7933390b"'
#latestBlockHashAnswer = '"0000000000000000013b476cf8af07a136c0cffd86ed6e268f5e6d4b02e4604f"'

if DEBUG != 0: print 'BLOCK HASH ->', latestBlockHashAnswer
if DEBUG != 0: print '-------------------------------------'



jsonBlockAnswer=getJsonBlock(latestBlockHashAnswer[1:65])

myBlock = blockClass()
myBlock.add(jsonBlockAnswer["hash"], jsonBlockAnswer["prev_block"], jsonBlockAnswer["time"])

myAddr = addrClass()
myTransaction = transactionClass()

transNum=0
for transList in jsonBlockAnswer["tx"]:
  if DEBUG != 0: print 'TRANS HASH ->', transList["hash"]
  if DEBUG != 0: print 'TIME       ->', transList["time"]
  for transInput in transList["inputs"]:
    if transNum==0 :
      transFrom='mine'
    else:
      try:
        transFrom=transInput["prev_out"]["addr"]
      except: transFrom='--ERR--'
    if DEBUG != 0: print 'IN ->',transFrom
    myAddr.add(transFrom)

  for transOut in transList["out"]:
    try:
      transTo=transOut["addr"]
      if DEBUG != 0: print 'OUT ->',transTo
      myAddr.add(transFrom)
    except: transTo='--ERR--'
    transVal=transOut["value"]
    transSpent=transOut["spent"]
    if DEBUG != 0: print 'VAL ->',transVal

  transNum=transNum+1
  myTransaction.add(transList["hash"], transFrom, transTo, transVal, transSpent, transList["time"])
  if DEBUG != 0: print '--------------------'

if DEBUG != 0: print myAddr.addrList
if DEBUG != 0: print myBlock.blockList
if DEBUG != 0: print myTransaction.transactionList
if DEBUG != 0: print "That's all folks!"