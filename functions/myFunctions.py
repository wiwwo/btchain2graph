#!/usr/bin/python
import requests, json, urllib2



####################################################################
def getLatestBlock():
  latestBlockUrl="https://blockchain.info/latestblock"

  response = urllib2.urlopen(latestBlockUrl)
  #return '00000000000107925a52e24c838788a954d1a6d5858301c66d50b2a074787460'
  #return '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'
  rawBlockAnswer = response.read()
  return json.loads(rawBlockAnswer)["hash"]


####################################################################
def getJsonBlock(p_block):
  rawBlockUrl="https://blockchain.info/rawblock/"

  response = urllib2.urlopen(rawBlockUrl+p_block)
  rawBlockAnswer = response.read()

  return json.loads(rawBlockAnswer)


####################################################################
def getOldestBlock(p_steps):
  blockUrl="https://blockchain.info/block-height/"+ str(p_steps) +"?format=json"

  response = urllib2.urlopen(blockUrl)
  rawBlockAnswer = response.read()
  return json.loads(rawBlockAnswer)["blocks"][0]["hash"]
