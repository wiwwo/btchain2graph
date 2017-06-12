class addrClass:

  def __init__(self):
    self.elemList = []

    self.header = []
    self.header.append('hash')

    self.elemListArr = []


  def add(self, p_hash):
    if p_hash not in self.elemListArr:
      self.elemList.append({self.header[0]: p_hash})
      self.elemListArr.append(p_hash)
