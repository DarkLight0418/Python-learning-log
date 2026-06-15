"""
Usecase 연산 결과 표준 모델.

Usecase는 Domain 객체를 조작한 뒤,
UI/Presenter가 사용할 수 있는 결과를 OperationResult 형태로 반환

입력값 검증
자료구조 조작
예외 처리
사용자에게 보여줄 메시지 생성
현재 snapshot 반환

2026.06.15 작성
"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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