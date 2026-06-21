'''
스택 좌표 계산(레이아웃)
2026.02.23. 최초 작성
'''

from __future__ import annotations
from dataclasses import dataclass
from vds.scene.models import Vec2, RectGeom

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
  
  
def compute_stack_layout(n_items: int, spec: StackLayoutSpec) -> StackLayout:
  """
  규칙:
    - 오른쪽 영역에 bottom-aligned로 쌓는다.
    - i=0(바닥)부터 위로 올라가며 배치한다.
    - TOP 포인터는 최상단 아이템의 왼쪽 중앙을 가리킨다.
      (아이템이 없으면 바닥 기준점을 가리킨다.)
  """
  
  # 오른쪽 스택 영역 좌표
  area_left = spec.scene_width - spec.margin - spec.stack_area_width
  area_top = spec.top_hud_height + spec.margin
  area_bottom = spec.scene_height - spec.margin
  
  # item 박스는 영역 안에서 가운데 정렬
  x = area_left + (spec.stack_area_width - spec.item_width) / 2.0

  item_geoms: list[RectGeom] = []
  for i in range(n_items):
    # bottom-aligned: 바닥에서 로 쌓기
    y = area_bottom - spec.item_height - i * (spec.item_height + spec.gap)
    
    item_geoms.append(
      RectGeom(
        pos=Vec2(x=x, y=y),
        size=Vec2(x=spec.item_width, y=spec.item_height),
      )
    )
    
  # TOP 포인터 타겟(아이템이 있으면 최상단, 없으면 바닥 기준)
  if n_items > 0:
      top_geom = item_geoms[-1]
      target_y = top_geom.pos.y + top_geom.size.y / 2.0
      target_x = top_geom.pos.x
  else:
      target_y = area_bottom - spec.item_height / 2.0
      target_x = x

  # TOP 포인터 배치 규칙
  # - 화살표 머리(end)는 스택 박스 왼쪽 근처
  # - 화살표 꼬리(start)는 그보다 왼쪽
  # - TOP 라벨은 화살표 꼬리보다 더 왼쪽
  arrow_to_box_gap = 10
  arrow_length = 48
  label_to_arrow_gap = 8

  arrow_end_x = target_x - arrow_to_box_gap
  arrow_start_x = arrow_end_x - arrow_length
  label_x = arrow_start_x - label_to_arrow_gap

  top_label_pos = Vec2(x=label_x, y=target_y)
  top_arrow_start = Vec2(x=arrow_start_x, y=target_y)
  top_arrow_end = Vec2(x=arrow_end_x, y=target_y)

  return StackLayout(
      spec=spec,
      item_geoms=tuple(item_geoms),
      top_label_pos=top_label_pos,
      top_arrow_start=top_arrow_start,
      top_arrow_end=top_arrow_end,
  )