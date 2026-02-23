'''
스택 좌표 계산(레이아웃)
2026.02.23. 최초 작성
'''

from __future__ import annotations
from dataclasses import dataclass
from vds.presenter.models import Vec2, RectGeom

@dataclass(frozen=True)
class StackLayoutSpec:
  # Scene 크기
  scene_width: int = 800
  scene_height: int = 600
  
  
  # 공통 여백
  margin: int = 32
  
  # 스택 영역 (오른쪽 패널)
  stack_area_width: int = 220
  
  # 스택 아이템 박스 크기/간격
  item_width: int = 140
  item_height: int = 44
  gap: int = 10
  
  # 상단 HUD(타이틀/복잡도) 공간 높이
  top_hud_height: int = 64
  
  
@dataclass(frozen=True)
class StackLayout:
  spec: StackLayoutSpec
  item_geoms: tuple[RectGeom, ...]  # i = 0이 bottom, i가 커질 수록 top
  top_label_pos: Vec2
  top_arrow_start: Vec2
  top_arrow_end: Vec2
  
