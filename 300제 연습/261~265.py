class Stock:
  def __init__(self, name, code):
    self.name = name
    self.code = code
  
  def set_name(self, name):
    self.name = name
  
  def set_code(self, code):
    self.code = code
    
  def get_name(self):
    return self.name
    
  def get_code(self):
    return self.code
    
    
SK = Stock("SK하이닉스", "0043234")
print(SK.name)
print(SK.code)
print(SK.get_name())
print(SK.get_code())
