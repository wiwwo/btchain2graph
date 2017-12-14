import requests, json
import time, datetime
import random


from myApiCalls import *

from blockClass import *
from addrClass import *
from transactionClass import *
from blockChainClass import *
from transaction2blockClass import *

import myGlobals, myLogger


####################################################################
def handleBlock (p_block):

  errNodeFound = 0

  myGlobals.logger.debug('Starting block ' + p_block)

  jsonBlockAnswer=getJsonBlock(p_block)

  myGlobals.logger.debug ('BLOCK HASH -> '+jsonBlockAnswer["hash"])
  myGlobals.logger.debug ('PREV BLOCK HASH -> '+jsonBlockAnswer["prev_block"])
  myGlobals.previousBlockHash = jsonBlockAnswer["prev_block"]

  # BLOCK node handling
  if jsonBlockAnswer["prev_block"] == '0000000000000000000000000000000000000000000000000000000000000000':
    myGlobals.myBlock.add('0000000000000000000000000000000000000000000000000000000000000000', '0')
  myGlobals.myBlock.add(jsonBlockAnswer["hash"], jsonBlockAnswer["time"])

  # BLOCKCHAIN relations handling
  myGlobals.myBlockChain.add(p_blockFrom = jsonBlockAnswer["hash"], p_blockTo = jsonBlockAnswer["prev_block"])


  # TRANSACTION node handling
  # Default address for exceptions
  myGlobals.myAddr.add('miner')
  myGlobals.myAddr.add('--ERR--')
  transNum=0
  for transList in jsonBlockAnswer["tx"]:
    myGlobals.logger.debug ('TRANS HASH -> '+ transList["hash"])
    myGlobals.logger.debug ('TIME -> '+ str(transList["time"]))
    for transInput in transList["inputs"]:
      if transNum==0 :
        transFrom='miner'
      else:
        try:
          transFrom=transInput["prev_out"]["addr"]
          myGlobals.myAddr.add(transFrom)
        except:
          transFrom='--ERR--'
          errNodeFound = 1
      myGlobals.logger.debug ('IN -> '+transFrom)


    for transOut in transList["out"]:
      try:
        transTo=transOut["addr"]
        myGlobals.logger.debug ('OUT -> '+str(transTo))
        myGlobals.myAddr.add(transTo)
      except:
        transTo='--ERR--'
        errNodeFound = 1
      transVal=transOut["value"]
      transSpent=transOut["spent"]
      myGlobals.logger.debug ('VAL -> '+str(transVal))

    transNum=transNum+1
    myGlobals.myTransaction.add(transFrom, transTo, transList["hash"], transVal, transSpent, jsonBlockAnswer["hash"], transList["time"])

    # TRANSACTION2BLOCK relatins handling
    myGlobals.myTransaction2block.add(transFrom, jsonBlockAnswer["hash"])
    myGlobals.logger.debug ('--------------------')
    return errNodeFound

