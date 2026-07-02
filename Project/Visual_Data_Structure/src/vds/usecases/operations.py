"""
Usecase 연산 결과 표준 모델.

Usecase는 Domain 객체를 조작한 뒤,
UI/Presenter가 사용할 수 있는 결과를 OperationResult 형태로 반환

입력값 검증
자료구조 조작
예외 처리
사용자에게 보여줄 메시지 생성
현재 snapshot 반환

2026.06.15 최초 작성
"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from enum import Enum


class OperationStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    
    
@dataclass(frozen=True)
class OperationResult:
    """
    Usecase 실행 결과.

    Attributes:
        operation:
            실행한 연산 이름. 예: "push", "pop", "top"
        status:
            성공/실패 상태.
        message:
            사용자에게 보여줄 수 있는 메시지.
        value:
            pop/top처럼 연산 결과로 나온 값.
        snapshot:
            연산 이후 자료구조의 현재 상태.
    """

    operation: str
    status: OperationStatus
    message: str = ""
    value: Any | None = None
    snapshot: tuple[Any, ...] = field(default_factory=tuple)
    
    @property
    def ok(self) -> bool:
        return self.status == OperationStatus.SUCCESS
    
    @property
    def failed(self) -> bool:
        return not self.ok
    
    # 성공하는 경우
    @classmethod
    def success(
        cls,
        operation: str,
        message: str = "",
        value: Any | None = None,
        snapshot: tuple[Any, ...] | list[Any] = (),
    ) -> "OperationResult":
        return cls(
            operation=operation,
            status=OperationStatus.SUCCESS,
            message=message,
            value=value,
            snapshot=tuple(snapshot),
        )
    
    
    # 실패하는 경우
    @classmethod
    def failure(
        cls,
        operation: str,
        message: str = "",
        value: Any | None = None,
        snapshot: tuple[Any, ...] | list[Any] = (),
    ) -> "OperationResult":
        return cls(
            operation=operation,
            status=OperationStatus.FAILURE,
            message=message,
            value=value,
            snapshot=tuple(snapshot),
        )
        
        
        
        
"""
(복습용 기록)

operations.py 공부 기록

이 파일은 Usecase가 작업한 결과를 담는 공통 결과 객체를 만든다.

Usecase가 직접 print하면 나중에 GUI나 웹으로 바꿀 때 문제가 생긴다.
그래서 Usecase는 화면에 직접 말하지 않고 OperationResult를 반환한다.

OperationResult에는 성공/실패, 메시지, 결과값, 현재 자료구조 상태가 들어간다.

즉, Usecase는 일을 하고 '결과 보고서'를 돌려준다.
화면에 어떻게 보여줄지는 Presenter나 UI가 결정한다.

오늘 이해한 문장:
Usecase는 요리사이고, OperationResult는 완성된 음식과 설명이 담긴 쟁반이다.

"""
