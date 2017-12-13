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
if loopDeep < 0: logger.info ('Going from genesis onwards!')


try:
  appendFlag=sys.argv[2][-1]
except:
  appendFlag='w'
logger.info ('Writing file in mode '+appendFlag)

sys.path.append( "functions" )
sys.path.append( "classes" )

from myFunctions import *
from blockClass import *
from addrClass import *
from transactionClass import *
from blockChainClass import *
from transaction2blockClass import *

myBlock = blockClass()
myAddr = addrClass()
myTransaction = transactionClass()
myBlockChain = blockChainClass()
myTransaction2block = transaction2blockClass ()

epochTime = int(time.time())
# File list
fileWriteList=[('addresses_nodes',myAddr),('blocks_nodes',myBlock),('transactions_rels',myTransaction),('blockchain_rels',myBlockChain),('transaction2block_rels',myTransaction2block)]

outputFileDir = 'output/'#+str(epochTime)
if not os.path.exists(outputFileDir):
    os.makedirs(outputFileDir)


myHeaderFile = {}
myDataFile = {}
# I open files here, so in case something is locking them, i won't waste elaboration
# that will eventually break
for thisFileName, thisCollection in fileWriteList:
  # Header files
  myHeaderFile[thisFileName] = open(outputFileDir + thisFileName + '.csv.header', 'w')
  # Data files
  myDataFile[thisFileName] = gzip.open(outputFileDir + thisFileName + '.csv.gz', appendFlag+'b')


soFar=0

# Negative depth meand "from genesis forward"
if loopDeep > 0:
  latestBlockHash = getLatestBlock()
else:
  loopDeep = abs(loopDeep)
  latestBlockHash = getOldestBlock(loopDeep-1)


for thisBlock in range (0, loopDeep):
  soFar=soFar+1
  logger.info('Starting block '+str(soFar)+'/'+str(loopDeep))

  jsonBlockAnswer=getJsonBlock(latestBlockHash)

  logger.debug ('BLOCK HASH -> '+jsonBlockAnswer["hash"])
  logger.debug ('PREV BLOCK HASH -> '+jsonBlockAnswer["prev_block"])

  # BLOCK node handling
  myBlock.add(jsonBlockAnswer["hash"], jsonBlockAnswer["time"])

  # Not to loose last elaborated blockTo for blockChain relation
  if thisBlock == (loopDeep-1):
    myBlock.add(jsonBlockAnswer["prev_block"], 0)

  # BLOCKCHAIN relations handling
  myBlockChain.add(p_blockFrom = jsonBlockAnswer["hash"], p_blockTo = jsonBlockAnswer["prev_block"])


  # TRANSACTION node handling
  # Default address for exceptions
  myAddr.add('--ERR--')
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
          myAddr.add(transFrom)
        except: transFrom='--ERR--'
      logger.debug ('IN -> '+transFrom)


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
    myTransaction.add(transFrom, transTo, transList["hash"], transVal, transSpent, jsonBlockAnswer["hash"], transList["time"])

    # TRANSACTION2BLOCK relatins handling
    myTransaction2block.add(transFrom, jsonBlockAnswer["hash"])
    logger.debug ('--------------------')

  # Check if reached genesis block
  if jsonBlockAnswer["prev_block"] == '0000000000000000000000000000000000000000000000000000000000000000':
    logger.info('Reached GENESIS block')

    # Check if i added genesis block before...
    if thisBlock != (loopDeep-1):
      myBlock.add(jsonBlockAnswer["prev_block"], 0)

    # Nothing before Genesis
    break

  # Altro giro, altra corsa
  latestBlockHash = jsonBlockAnswer["prev_block"]


# Write it down now! :-)
for thisFileName, thisCollection in fileWriteList:

  # Data files
  logger.info('Now spooling '+thisFileName+'.csv.gz')
  wr = csv.writer(myDataFile[thisFileName], quoting=csv.QUOTE_ALL)
  for row in thisCollection.elemList:
    wr.writerow(row.values())
  myDataFile[thisFileName].close()

  # Header files
  wr = csv.writer(myHeaderFile[thisFileName], quoting=csv.QUOTE_ALL)
  wr.writerow(thisCollection.elemList[0].keys())
  myHeaderFile[thisFileName].close()



logger.info("That's all folks!")