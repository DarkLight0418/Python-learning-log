"""
Stack Usecase.

UI나 Controller가 Stack을 직접 조작하지 않고,
이 Usecase를 통해 push/pop/top 등의 명령을 실행하도록 한다.

2026.06.16 작성

"""

from __future__ import annotations

from typing import Any

from vds.core.errors import EmptyStackError
from vds.core.stack import Stack
from vds.usecases.operations import OperationResult

class StackUsecase:
    """
    Stack 자료구조 조작을 담당하는 Application 계층 객체.

    책임:
        - 입력값 검증
        - Stack 조작
        - Domain 예외 처리
        - UI/Presenter에 전달할 결과 생성

    책임이 아닌 것:
        - Scene 생성
        - Canvas 렌더링
        - Tkinter 위젯 조작
    
        -> 즉 UI 쪽을 직접 건드리지 말아야 해용.
    """
    
    def __init__(self, stack: Stack | None = None):
        self._stack = stack or Stack()
        
    def push(self, raw_value: Any) -> OperationResult:
        """
        Stack에 값 추가

        문자열 입력의 경우 앞뒤 공백을 제거하고,
        빈 문자열은 실패로 처리.
        """
        
        value = self._normalize_value(raw_value)
        
        if value is None:
            return OperationResult.failure(
                operation="push",
                message="push할 값을 입력하세요.",
                snapshot=self.snapshot(),
            )
            
        self._stack.push(value)
        
        return OperationResult.success(
            operation="push",
            message=f"{value} 값을 push했습니다.",
            value=value,
            snapshot=self.snapshot(),
        )
        
    def pop(self) -> OperationResult:
        """
        Stack의 top 값을 제거하고 반환

        Stack이 비어 있으면 예외를 밖으로 던지지 않고,
        실패 결과로 변환.
        """
        
    def top(self) -> OperationResult:
        """
        Stack의 top 값 조회.

        값을 제거하지는 않음.
        """
        
        try:
            top_value = self._stack.top()
        except EmptyStackError as error:
            return OperationResult.failure(
                operation="top",
                message=str(error),
                snapshot=self.snapshot(),
            )
            
        return OperationResult.success(
            operation="top",
            message=f"현재 top값은 {top_value}입니다.",
            value=top_value,
            snapshot=self.snapshot(),
        )
        
    def clear(self) -> OperationResult:
        """
        Stack을 비움.

        현재 Stack 클래스에 clear 메서드가 없으므로,
        pop을 반복해서 비움.
        """
        
        while not self._stack.is_empty():
            self._stack.pop()
            
        return OperationResult.success(
            operation="clear",
            message="스택을 초기화했습니다.",
            snapshot=self.snapshot(),
        )
        
    def snapshot(self) -> tuple[Any, ...]:
        """
        현재 Stack 상태를 불변 tuple로 반환.

        Presenter는 이 snapshot을 받아 Scene으로 변환.
        """
        
        return tuple(self._stack.snapshot())
        
    def size(self) -> int:
        return self._stack.size()
    
    def is_empty(self) -> bool:
        return self._stack.is_empty()
    
    def _normalize_value(self, raw_value: Any) -> Any | None:
        """
        UI 입력값을 Stack에 넣을 값으로 정리.

        현재 MVP에서는 문자열 입력을 주로 가정.
        """
        if raw_value is None:
            return None
        
        if isinstance(raw_value, str):
            value = raw_value.strip()
            if value == "":
                return None
            return value
        
        return raw_value