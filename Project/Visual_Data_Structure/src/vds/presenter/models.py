"""
Drawable 모델 코드
2026.02.21 최초 작성
"""

from __future__ import annotations  # 타입 힌트를 문자열처럼 늦게 평가하게끔 설정

from dataclasses import dataclass, field  # 값 객체(VO) 만들기 자동화(DTO 자동 생성과 같이)
from typing import Literal, Optional, Union, List, Dict, Tuple  # typing(타입 힌트)


''' 기본 그림 구조 벡터 클래스(Basic geometry) '''

@dataclass(frozen=True)
class Vec2:
  x: float
  y: float
  
@dataclass(frozen=True)
class RectGeom:
  pos: Vec2    # top-left
  size: Vec2   # width/height


''' Style Tokens (role 기반 매핑) '''
StrokeCap = Literal["butt", "round", "square"]
TextAlign = Literal["left", "center", "right"]

@dataclass(frozen=True)
class Stroke:
  width: float = 2.0
  cap: StrokeCap = "round"
  dashed: bool = False
  
@dataclass(frozen=True)
class Style:
  role: str = "default"
  fill: Optional[str] = None
  outline: Optional[str] = None
  text: Optional[str] = None
  stroke: Stroke = Stroke()
  
''' Drawable items(그릴 최소 단위 도형 3가지) '''
@dataclass(frozen=True)
class RectItem:
  key: str
  geom: RectGeom
  style: Style = Style(role="rect")
  z: int = 0
  
@dataclass(frozen=True)
class TextItem:
  key: str
  pos: Vec2
  text: str
  style: Style = Style(role="text")
  align: TextAlign = "center"
  z: int = 10
  
@dataclass(frozen=True)
class ArrowItem:
  key: str
  start: Vec2
  end: Vec2
  style: Style = Style(role="arrow")
  head_size: float = 10.0
  z: int = 5
  
  
Drawable = Union[RectItem, TextItem, ArrowItem]

