class blockClass:

  def __init__(self):
    self.blockList = [{}]


  def add (self, p_hash, p_prev_block, p_time):

    #Block hash is unique...
    #if p_hash not in self.blockList:
    self.blockList.append({'hash': p_hash, 'prev_block': p_prev_block, 'time': p_time})
