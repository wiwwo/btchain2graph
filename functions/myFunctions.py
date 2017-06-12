#!/usr/bin/python
import requests, json, urllib2



####################################################################
def getLatestBlock():
  latestBlockUrl="https://blockchain.info/latestblock"

  response = urllib2.urlopen(latestBlockUrl)
  # TODO - This sucks, but "Need for Speed"
  return response.read()[15:81]
  #return '"00000000000107925a52e24c838788a954d1a6d5858301c66d50b2a074787460"'


####################################################################
def getJsonBlock(p_block):
  rawBlockUrl="https://blockchain.info/rawblock/"

  response = urllib2.urlopen(rawBlockUrl+p_block)
  rawBlockAnswer = response.read()

  return json.loads(rawBlockAnswer)


####################################################################
def getBlock(p_blockHash):
  blockUrl="https://blockchain.info/rawblock/"

  response = urllib2.urlopen(blockUrl+p_blockHash)
  # TODO - This sucks, but "Need for Speed"
  return response.read()[15:81]
