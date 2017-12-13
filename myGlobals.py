import logging, sys

sys.path.append( "classes" )

from blockClass import *
from addrClass import *
from transactionClass import *
from blockChainClass import *
from transaction2blockClass import *

global logger
logger = logging.getLogger('')

myBlock = blockClass()
myAddr = addrClass()
myTransaction = transactionClass()
myBlockChain = blockChainClass()
myTransaction2block = transaction2blockClass ()

previousBlockHash = ''