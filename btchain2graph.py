#!/usr/bin/python

import requests, json, urllib2, csv
import time, datetime
import gzip, sys, os, getopt
import random

import myGlobals
import _Params

sys.path.append( "functions" )
sys.path.append( "classes" )

import myLogger
import myApiCalls
import blockHandling


# File list
fileWriteList=[ ('addresses.nodes',         myGlobals.myAddr)
               ,('blocks.nodes',            myGlobals.myBlock)
               ,('transactions.rels',       myGlobals.myTransaction)
               ,('blockchain.rels',         myGlobals.myBlockChain)
               ,('transaction2block.rels',  myGlobals.myTransaction2block)
              ]


def main(argv):

  epochTime = int(time.time())

  myLogger.startLogger ()
  myGlobals.logger.info('Hello you!')


  try:
    startHeight=int(sys.argv[1])
  except:
    startHeight = 0
  myGlobals.logger.info ('Start height: '+str(startHeight))

  try:
    endHeight=int(sys.argv[2])
  except:
    endHeight = blockHandling.getLatestBlockHeight()
  myGlobals.logger.info ('End   height: '+str(endHeight))


  epochTime = int(time.time())

  outputFileDir = 'output/'
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
    #myDataFile[thisFileName] = gzip.open(filename=outputFileDir + thisFileName + '.csv.gz', mode='wb', compresslevel=_Params.compressionLevel)
    myDataFile[thisFileName] = gzip.open(filename=('%s%07d-%07d.%s.csv.gz' % (outputFileDir, startHeight, endHeight, thisFileName)), mode='wb', compresslevel=_Params.compressionLevel)


  blocksSoFar=spooledCounter=blockWithErrNode = 0

  listFile = open(outputFileDir + '_execution-'+str(epochTime)+'.log', 'w')


  for thisHeight in range (startHeight, endHeight+1):
    blocksSoFar=blocksSoFar+1
    spooledCounter=spooledCounter+1

    strLenTotal=len(str(endHeight-startHeight+1))
    myGlobals.logger.debug('Going for height %07d - %0'+str(strLenTotal)+'d/%0'+str(strLenTotal)+'d', thisHeight, blocksSoFar, endHeight-startHeight+1)


    blockHash = blockHandling.getBlockByHeight(thisHeight)
    blockWithErrNode = blockHandling.handleBlock (blockHash)

    if blocksSoFar == 1:
      # Header files
      for thisFileName, thisCollection in fileWriteList:
        myGlobals.logger.debug('Now spooling '+thisFileName+'.csv.header')
        wr = csv.writer(myHeaderFile[thisFileName], quoting=csv.QUOTE_ALL)
        wr.writerow(thisCollection.elemList[0].keys())
        myHeaderFile[thisFileName].close()


    if spooledCounter == _Params.spoolEvery:
      # Data files
      myGlobals.logger.info('Now spooling files - done so far: '+str(blocksSoFar))
      for thisFileName, thisCollection in fileWriteList:
        myGlobals.logger.debug('Now spooling '+thisFileName+'.csv.gz')
        wr = csv.writer(myDataFile[thisFileName], quoting=csv.QUOTE_ALL)
        for row in thisCollection.elemList:
          wr.writerow(row.values())
        thisCollection.elemList=[]

      spooledCounter = 0
      listFile.flush()

    listFile.write('%d\t%07d\t%d\n' % (int(time.time()), thisHeight, blockWithErrNode))


  # Write it down now! :-)
  myGlobals.logger.info('Now spooling files')
  for thisFileName, thisCollection in fileWriteList:

    # Data files
    myGlobals.logger.debug('Now spooling '+thisFileName+'.csv.gz')
    wr = csv.writer(myDataFile[thisFileName], quoting=csv.QUOTE_ALL)

    for row in thisCollection.elemList:
      wr.writerow(row.values())
    thisCollection.elemList=[]
    myDataFile[thisFileName].close()


  listFile.close()
  myGlobals.logger.info("That's all folks!")


if __name__ == "__main__":
    main(sys.argv)