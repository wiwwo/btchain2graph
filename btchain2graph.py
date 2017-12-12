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
from blockChainClass import *

myBlock = blockClass()
myAddr = addrClass()
myTransaction = transactionClass()
myBlockChain = blockChainClass()

fileWriteList=[('addresses',myAddr),('block',myBlock),('transactions',myTransaction),('blockchain',myBlockChain)]

# I open files here, so in case something is locking them, i won't waste elaboration
# that will eventually break
for thisFileName, thisCollection in fileWriteList:
  with gzip.open('output/'+thisFileName+'.csv.gz', 'wb') as myfile: myfile.close()


soFar=0
latestBlockHash = getLatestBlock()

for thisBlock in range (0, loopDeep):
  soFar=soFar+1
  logger.info('Starting block '+str(soFar)+'/'+str(loopDeep))

  latestBlockHashAnswer = getBlock(latestBlockHash)
  jsonBlockAnswer=getJsonBlock(latestBlockHashAnswer)

  logger.debug ('BLOCK HASH -> '+latestBlockHashAnswer)
  logger.debug ('PREV BLOCK HASH -> '+jsonBlockAnswer["prev_block"])

  # BLOCK node handling
  myBlock.add(jsonBlockAnswer["hash"], jsonBlockAnswer["time"])

  # Not to loose last elaborated blockTo for blockChain relation
  if thisBlock == (loopDeep-1):
    myBlock.add(jsonBlockAnswer["prev_block"], 0)

  # BLOCKCHAIN relations handling
  myBlockChain.add(p_blockFrom = jsonBlockAnswer["hash"], p_blockTo = jsonBlockAnswer["prev_block"])


  # TRANSACTION node handling
  transNum=0
  for transList in jsonBlockAnswer["tx"]:
    logger.debug ('TRANS HASH -> '+ transList["hash"])
    logger.debug ('TIME -> '+ str(transList["time"]))
    for transInput in transList["inputs"]:
      if transNum==0 :
        transFrom='miner'
      else:
        try:
          transFrom=transInput["prev_out"]["addr"]
        except: transFrom='--ERR--'
      logger.debug ('IN -> '+transFrom)
      myAddr.add(transFrom)

    for transOut in transList["out"]:
      try:
        transTo=transOut["addr"]
        logger.debug ('OUT -> '+str(transTo))
        myAddr.add(transTo)
      except: transTo='--ERR--'
      transVal=transOut["value"]
      transSpent=transOut["spent"]
      logger.debug ('VAL -> '+str(transVal))

    transNum=transNum+1
    myTransaction.add(transFrom, transTo, transList["hash"], transVal, transSpent, transList["time"])
    logger.debug ('--------------------')

  # Check if reached genesis block
  if jsonBlockAnswer["prev_block"] == '0000000000000000000000000000000000000000000000000000000000000000':
    logger.info('Reached GENESIS block')

    # Check if i added genesis block before...
    if thisBlock != (loopDeep-1):
      myBlock.add(jsonBlockAnswer["prev_block"], 0)

    # Nothing before Genesis
    break

  # Alro giro, altra corsa
  latestBlockHash = jsonBlockAnswer["prev_block"]


# Write it down now! :-)
for thisFileName, thisCollection in fileWriteList:

  with gzip.open('output/'+thisFileName+'.csv.gz', 'wb') as myfile:
    logger.info('Now spooling '+thisFileName+'.csv.gz')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(thisCollection.elemList[0].keys())
    for row in thisCollection.elemList:
      wr.writerow(row.values())
    myfile.close()


logger.info("That's all folks!")