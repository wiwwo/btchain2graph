class transactionClass:

  def __init__(self):
    self.transactionList = []

    self.header = []
    self.header.append('hash')
    self.header.append('addrFrom')
    self.header.append('addrTo')
    self.header.append('value')
    self.header.append('spent')
    self.header.append('time')


  def add (self, p_hash, p_addrFrom, p_addrTo, p_value, p_spent, p_time):

    # Transactio hash is unique...
    #if p_hash not in self.transactionList:
    self.transactionList.append({self.header[0]: p_hash, self.header[1]: p_addrFrom, self.header[2]: p_addrTo, self.header[3]: p_value, self.header[4]: p_spent, self.header[5]: p_time})
