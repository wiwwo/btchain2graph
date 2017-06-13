#!/usr/bin/python

import logging

import requests, json, urllib2, csv
import time, datetime
import gzip, sys, os, getopt
import random

logger = logging.getLogger('')
logger.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s [%(relativeCreated)12d] - %(message)s")

argv0=os.path.basename(sys.argv[0 ])
ch = logging.StreamHandler(sys.stdout)
ch2 = logging.FileHandler('log/'+datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')+'_'+argv0+'.log')
ch.setFormatter(format)
ch2.setFormatter(format)
logger.addHandler(ch)
logger.addHandler(ch2)

logger.info('Hello you!')

try:
  logger.debug ('Depth by param')
  loopDeep=int(sys.argv[1])
except:
  logger.debug ('Depth by default')
  loopDeep=5
logger.info ('Depth: '+str(loopDeep))

sys.path.append( "functions" )
sys.path.append( "classes" )

from myFunctions import *
from blockClass import *
from addrClass import *
from transactionClass import *


myBlock = blockClass()
myAddr = addrClass()
myTransaction = transactionClass()

soFar=0
for thisBlock in range (0, loopDeep):
  soFar=soFar+1
  logger.info('Starting block '+str(soFar)+'/'+str(loopDeep))
  if thisBlock == 0:  latestBlockHashAnswer = getLatestBlock()
  else:               latestBlockHashAnswer = getBlock(jsonBlockAnswer["prev_block"])
  if latestBlockHashAnswer[0]+latestBlockHashAnswer[65] != '""': exit
  logger.debug ('BLOCK HASH ->', latestBlockHashAnswer)

  jsonBlockAnswer=getJsonBlock(latestBlockHashAnswer[1:65])

  myBlock.add(jsonBlockAnswer["hash"], jsonBlockAnswer["prev_block"], jsonBlockAnswer["time"])

  transNum=0
  for transList in jsonBlockAnswer["tx"]:
    logger.debug ('TRANS HASH ->', transList["hash"])
    logger.debug ('TIME       ->', transList["time"])
    for transInput in transList["inputs"]:
      if transNum==0 :
        transFrom='mine'
      else:
        try:
          transFrom=transInput["prev_out"]["addr"]
        except: transFrom='--ERR--'
      logger.debug ('IN ->',transFrom)
      myAddr.add(transFrom)

    for transOut in transList["out"]:
      try:
        transTo=transOut["addr"]
        logger.debug ('OUT ->',transTo)
        myAddr.add(transTo)
      except: transTo='--ERR--'
      transVal=transOut["value"]
      transSpent=transOut["spent"]
      logger.debug ('VAL ->',transVal)

    transNum=transNum+1
    myTransaction.add(transList["hash"], transFrom, transTo, transVal, transSpent, transList["time"])
    logger.debug ('--------------------')
  if jsonBlockAnswer["prev_block"] == '0000000000000000000000000000000000000000000000000000000000000000':
    logger.info('Reached GENESIS block')
    break

for thisFileName, thisCollection in [('addresses',myAddr),('block',myBlock),('transactions',myTransaction)]:

  with gzip.open('output/'+thisFileName+'.csv.gz', 'wb') as myfile:
    logger.info('Now spooling '+thisFileName+'.csv.gz')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(thisCollection.header)
    for row in thisCollection.elemList:
      wr.writerow(row.values())

logger.info("That's all folks!")