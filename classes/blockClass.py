class blockClass:

  def __init__(self):
    self.label='block'
    self.elemList = []

    self.header = []
    self.header.append(':LABEL')
    self.header.append('id:id(block)')
    self.header.append('prev_block')
    self.header.append('time')


  def add (self, p_hash, p_prev_block, p_time):

    #Block hash is unique...
    #if p_hash not in self.elemList:
    self.elemList.append({self.header[0]: self.label, self.header[1]: p_hash, self.header[2]: p_prev_block, self.header[3]: p_time})
