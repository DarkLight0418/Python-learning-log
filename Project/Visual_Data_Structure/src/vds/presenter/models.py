"""
Drawable 모델 코드
2026.02.21 최초 작성
"""

from __future__ import annotations  # 타입 힌트를 문자열처럼 늦게 평가하게끔 설정

from dataclasses import dataclass, field  # 값 객체(VO) 만들기 자동화(DTO 자동 생성과 같이)
from typing import Literal, Optional, Union, List, Dict, Tuple  # typing(타입 힌트)

# 기본 그림 구조 벡터 클래스(Basic geometry)

@dataclass(frozen=True)
class Vec2:
  x: float
  y: float
  
@dataclass(frozen=True)
class RectGeom:
  pos: Vec2    # top-left
  size: Vec2   # width/height
