class transaction2blockClass:

  def __init__(self):
    self.label='transaction2block'
    self.address='address'
    self.block  ='block'
    self.elemList = []

    self.header = []
    self.header.append(':TYPE')
    self.header.append(':START_ID('+self.address+')')
    self.header.append(':END_ID('+self.block+')')



  def add (self, p_address, p_block):

    # Transactio hash is unique...
    #if p_hash not in self.elemList:
    self.elemList.append({self.header[0]: self.label, self.header[1]: p_address, self.header[2]: p_block})
