class addrClass:

  def __init__(self):
    self.label='address'
    self.elemList = []

    self.header = []
    self.header.append(':LABEL')
    self.header.append('id:id('+self.label+')')

    self.elemListArr = []


  def add(self, p_hash):
    if p_hash not in self.elemListArr:
      self.elemList.append({self.header[0]: self.label, self.header[1]: p_hash})
      self.elemListArr.append(p_hash)
