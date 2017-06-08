class addrClass:

  def __init__(self):
    self.addrList = [{}]


  def add(self, p_hash):
    if p_hash not in self.addrList:
      self.addrList.append({'hash': p_hash})
