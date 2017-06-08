#!/usr/bin/python
import requests, json, urllib2

def getLatestBlock():
  latestBlockUrl="https://blockchain.info/latestblock"

  response = urllib2.urlopen(latestBlockUrl)
  # TODO - This sucks, but "Need for Speed"
  return response.read()[15:81]

def getJsonBlock(p_block):
  rawBlockUrl="https://blockchain.info/rawblock/"

  response = urllib2.urlopen(rawBlockUrl+p_block)
  rawBlockAnswer = response.read()

  return json.loads(rawBlockAnswer)

