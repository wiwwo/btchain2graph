import os
import logging
import sys
import datetime

import myGlobals



def startLogger():

  myGlobals.logger.setLevel(logging.INFO)
  format = logging.Formatter("%(asctime)s [%(relativeCreated)12d] - %(message)s")

  argv0=os.path.basename(sys.argv[0 ])
  ch = logging.StreamHandler(sys.stdout)
  ch2 = logging.FileHandler('log/'+datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')+'_'+argv0+'.log')
  ch.setFormatter(format)
  ch2.setFormatter(format)
  myGlobals.logger.addHandler(ch)
  myGlobals.logger.addHandler(ch2)