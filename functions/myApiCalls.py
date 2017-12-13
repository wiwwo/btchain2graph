import requests, json, urllib2

global logger


####################################################################
def getLatestBlockHash():
  latestBlockUrl="https://blockchain.info/latestblock"

  response = urllib2.urlopen(latestBlockUrl)
  #return '00000000000107925a52e24c838788a954d1a6d5858301c66d50b2a074787460'
  #return '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f' # 1 block to genesis
  #return '0000000082b5015589a3fdf2d4baff403e6f0be035a5d9742c1cae6295464449' # 3 blocks to genesis
  rawBlockAnswer = response.read()
  return json.loads(rawBlockAnswer)["hash"]


####################################################################
def getLatestBlockHeight():
  latestBlockUrl="https://blockchain.info/latestblock"

  response = urllib2.urlopen(latestBlockUrl)
  #return '00000000000107925a52e24c838788a954d1a6d5858301c66d50b2a074787460'
  #return '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f' # 1 block to genesis
  #return '0000000082b5015589a3fdf2d4baff403e6f0be035a5d9742c1cae6295464449' # 3 blocks to genesis
  rawBlockAnswer = response.read()
  return json.loads(rawBlockAnswer)["height"]


####################################################################
def getJsonBlock(p_block):
  rawBlockUrl="https://blockchain.info/rawblock/"

  response = urllib2.urlopen(rawBlockUrl+p_block)
  rawBlockAnswer = response.read()

  return json.loads(rawBlockAnswer)


####################################################################
def getBlockByHeight(p_height):
  blockUrl="https://blockchain.info/block-height/"+ str(p_height) +"?format=json"

  response = urllib2.urlopen(blockUrl)
  rawBlockAnswer = response.read()
  return json.loads(rawBlockAnswer)["blocks"][0]["hash"]

