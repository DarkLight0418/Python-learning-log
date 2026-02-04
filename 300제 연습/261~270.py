class Stock:
  def __init__(self, name, code, per, pbr, 배당수익률):
    self.name = name
    self.code = code
    self.per = per
    self.pbr = pbr
    self.배당수익률 = 배당수익률
  
  def set_name(self, name):
    self.name = name
  
  def set_code(self, code):
    self.code = code
    
  def get_name(self):
    return self.name
    
  def get_code(self):
    return self.code
    
    
SK = Stock("SK하이닉스", "0043234", 15.79, 1.33, 2.83)
print(SK.name)
print(SK.code)
print(SK.배당수익률)

print(SK.get_name())
print(SK.get_code())
