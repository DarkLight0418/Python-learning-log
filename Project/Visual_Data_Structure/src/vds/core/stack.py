"""
스택 클래스, 예외 코드
2026.02.21 최초 작성
"""

class EmptyStackError(Exception):
  pass

class Stack:
  def __init__(self):
    self._data = []
    
  def push(self, value):
    self._data.append(value)
    
  def pop(self):
    if self.is_empty():
      raise EmptyStackError("스택이 비어있습니다.")
    return self._data.pop()
  
  def top(self):
    if self.is_empty():
      raise EmptyStackError("스택이 비어있습니다.")
    return self._data[-1]
  
  def is_empty(self):
    return len(self._data) == 0
  
  def size(self):
    return len(self._data)
  
  def snapshot(self):
    # Presenter용 안전 복사 메소드
    return list(self._data)