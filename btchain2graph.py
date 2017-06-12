#!/usr/bin/python

import logging

import requests, json, urllib2, csv
import time, datetime
import gzip, sys, os, getopt
import random

DEBUG=0
loopDeep=5

sys.path.append( "functions" )
sys.path.append( "classes" )

from myFunctions import *
from blockClass import *
from addrClass import *
from transactionClass import *


myBlock = blockClass()
myAddr = addrClass()
myTransaction = transactionClass()


for thisBlock in range (0, loopDeep):
  if thisBlock == 0:  latestBlockHashAnswer = getLatestBlock()
  else:               latestBlockHashAnswer = getBlock(jsonBlockAnswer["prev_block"])
  if latestBlockHashAnswer[0]+latestBlockHashAnswer[65] != '""': exit
  if DEBUG != 0: print 'BLOCK HASH ->', latestBlockHashAnswer
  if DEBUG != 0: print '-------------------------------------'

  jsonBlockAnswer=getJsonBlock(latestBlockHashAnswer[1:65])

  myBlock.add(jsonBlockAnswer["hash"], jsonBlockAnswer["prev_block"], jsonBlockAnswer["time"])

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


#print myAddr.addrList
#print myBlock.blockList
#print myTransaction.transactionList

with open('addresses.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(myAddr.header)
    for row in myAddr.elemList:
      wr.writerow(row.values())

with open('block.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(myBlock.header)
    for row in myBlock.elemList:
      wr.writerow(row.values())

with open('transactions.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(myTransaction.header)
    for row in myTransaction.elemList:
      wr.writerow(row.values())

print "That's all folks!"