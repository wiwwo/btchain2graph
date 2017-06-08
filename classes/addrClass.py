class addrClass:

  def __init__(self):
    self.addrList = [{}]
    self.addrListArr = []


  def add(self, p_hash):
    if p_hash not in self.addrListArr:
      self.addrList.append({'hash': p_hash})
      self.addrListArr.append(p_hash)
