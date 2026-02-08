from typing import Any

class FixedStack:
    # 고정 길이 스택 클래스
    
    class Empty(Exception):
        """스택이 비어 있을 때 pop 또는 peek을 호출하면 발생하는 예외"""
        pass
    
    class Full(Exception):
        """스택이 가득 찼을 때 push를 호출하면 발생하는 예외"""
        pass
    
    def __init__(self, capacity: int = 256) -> None:
        """스택 초기화 (기본 용량: 256)"""
        self.stk = [None] * capacity  # 스택 저장을 위한 리스트
        self.capacity = capacity  # 스택의 최대 크기
        self.ptr = 0  # 스택의 현재 요소 개수를 나타내는 포인터
        
    def __len__(self) -> int:
        """스택에 저장된 데이터 개수를 반환"""
        return self.ptr
    
    def is_empty(self) -> bool:
        """스택이 비어 있는지 확인"""
        return self.ptr <= 0
    
    def is_full(self) -> bool:
        """스택이 가득 찼는지 확인"""
        return self.ptr >= self.capacity
    
    def push(self, value: Any) -> None:
        """스택에 데이터를 추가 (가득 차 있으면 예외 발생)"""
        if self.is_full():  # self.is_full 대신 self.is_full()로 호출해야 함
            raise FixedStack.Full  # 예외 처리
        self.stk[self.ptr] = value  # 데이터를 스택에 추가
        self.ptr += 1  # 포인터 증가
        
    def pop(self) -> Any:
        """스택에서 데이터를 꺼내 반환 (비어 있으면 예외 발생)"""
        if self.is_empty():  # self.is_empty 대신 self.is_empty()로 호출해야 함
            raise FixedStack.Empty  # 예외 처리
        self.ptr -= 1  # 포인터 감소
        return self.stk[self.ptr]  # 꺼낸 데이터 반환
    
    def peek(self) -> Any:
        """스택의 맨 위 데이터를 확인 (비어 있으면 예외 발생)"""
        if self.is_empty():  # self.is_empty 대신 self.is_empty()로 호출해야 함
            raise FixedStack.Empty  # 예외 처리
        return self.stk[self.ptr - 1]  # 맨 위 데이터 반환
    
    def clear(self) -> None:
        """스택을 비움"""
        self.ptr = 0  # 포인터를 초기화하여 모든 데이터를 제거한 효과
        