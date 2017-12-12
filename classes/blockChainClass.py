class blockChainClass:

  def __init__(self):
    self.label='blockchain'
    self.blockFrom='block'
    self.blockTo  ='block'
    self.elemList = []

    self.header = []
    self.header.append(':TYPE')
    self.header.append(':START_ID('+self.blockFrom+')')
    self.header.append(':END_ID('+self.blockTo+')')


  def add (self, p_blockFrom, p_blockTo):

    #Block hash is unique...
    #if p_hash not in self.elemList:
    self.elemList.append({self.header[0]: self.label, self.header[1]: p_blockFrom, self.header[2]: p_blockTo})
