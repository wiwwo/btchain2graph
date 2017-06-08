class addrClass:

  def __init__(self):
    self.addrList = [{}]

    self.header = []
    self.header.append('hash')

    self.addrListArr = []


  def add(self, p_hash):
    if p_hash not in self.addrListArr:
      self.addrList.append({self.header[0]: p_hash})
      self.addrListArr.append(p_hash)
