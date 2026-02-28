'''
도메인 예외 처리 코드
'''

class DomainError(Exception):
    """모든 도메인 예외의 최상위 클래스"""
    pass

class EmptyStackError(Exception):
  def __init__(self, message="스택이 비어있습니다."):
    super().__init__(message)


