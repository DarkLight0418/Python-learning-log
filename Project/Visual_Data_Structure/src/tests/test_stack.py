"""
스택 테스트 코드
2026.02.21 최초 작성
"""


from vds.core.stack import Stack
from vds.core.errors import EmptyStackError
import pytest

def test_push_pop():
  s = Stack()
  s.push(10)
  s.push(20)
  
  # assert - 무조건 참이다 라고 가정함.
  
  assert s.pop() == 20
  assert s.pop() == 10

def test_empty_pop():
  s = Stack()
  with pytest.raises(EmptyStackError):
    s.pop()