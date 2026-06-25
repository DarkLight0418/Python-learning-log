from vds.core.errors import EmptyStackError, StackOverflowError
from dataclasses import dataclass

"""
스택 클래스, 예외 코드
2026.02.21 최초 작성
"""

@dataclass(frozen=True)
class StackNode:
  id: str
  value: object
  

class Stack:
  def __init__(self, capacity: int = 5):
    if capacity <= 0:
      raise ValueError("스택 용량은 1 이상이어야 합니다.")
    
    self._capacity = capacity
    self._data = []
    
  def push(self, value):
    if self.is_full():
      raise StackOverflowError("스택이 가득 찼습니다.")
    
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
  
  def is_full(self):
    return len(self._data) >= self._capacity
  
  def size(self):
    return len(self._data)
  
  def capacity(self):
    return self._capacity
  
  def remaining_capacity(self):
    return self._capacity - len(self._data)
  
  def snapshot(self):
    # Presenter용 안전 복사 메소드
    return list(self._data)