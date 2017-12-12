class transactionClass:

  def __init__(self):
    self.label='transaction'
    self.nodeFrom='address'
    self.nodeTo  ='address'
    self.elemList = []

    self.header = []
    self.header.append(':TYPE')
    self.header.append(':START_ID('+self.nodeFrom+')')
    self.header.append(':END_ID('+self.nodeTo+')')
    self.header.append('hash')
    self.header.append('value')
    self.header.append('spent')
    self.header.append('block')
    self.header.append('time')


  def add (self, p_addrFrom, p_addrTo, p_hash, p_value, p_spent, p_block, p_time):

    # Transactio hash is unique...
    #if p_hash not in self.elemList:
    self.elemList.append({self.header[0]: self.label, self.header[1]: p_addrFrom, self.header[2]: p_addrTo, self.header[3]: p_hash, self.header[4]: p_value, self.header[5]: p_spent, self.header[6]: p_block, self.header[7]: p_time})
