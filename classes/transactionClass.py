class transactionClass:

  def __init__(self):
    self.transactionList = [{}]


  def add (self, p_hash, p_addrFrom, p_addrTo, p_value, p_spent, p_time):

    # Transactio hash is unique...
    #if p_hash not in self.transactionList:
    self.transactionList.append({'hash': p_hash, 'addrFrom': p_addrFrom, 'addrTo': p_addrTo, 'value': p_value, 'spent': p_spent, 'time': p_time})
