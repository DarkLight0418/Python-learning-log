from dataclasses import dataclass
from __future__ import annotations

'''
색/폰트/간격 상수

2026.03.09. 최초 작성
'''


@dataclass(frozen=True)
class RoleTheme:
  """
  role -> (fill, outline, text) 기본 매핑
    - Style.fill/outline/text가 명시되어 있으면 그 값을 우선하도록 처리.
    - 없으면 role 기반으로 여기 기본값을 사용.
  """
  rect_fill: str = ""
  rect_outline: str = "black"
  text_color: str = "black" 
  