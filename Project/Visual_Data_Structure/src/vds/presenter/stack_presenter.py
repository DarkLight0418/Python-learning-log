'''
Stack Presenter: Stack 상태(list) -> Scene(Drawable)
2026.02.23 최초 작성
'''

from __future__ import annotations
from vds.utils.scene_models import (
  Vec2,
  RectItem,
  TextItem,
  ArrowItem,
  Style,
  Scene,
  SceneMeta,
)

from vds.presenter.layout.stack_layout import StackLayoutSpec, compute_stack_layout

class StackPresenter:
  def __init__(self, spec: StackLayoutSpec | None = None):
    self._spec = spec or StackLayoutSpec()
    
  def present_from_values(self, values: list[object]) -> Scene:
    """_summary_

    Args:
        values (list[object]): _description_

    Returns:
        Scene(장면): _description(설명)_
    """
    
    
    layout = compute_stack_layout(n_items=len(values), spec=self._spec)
    
    items = []
    
    # --- 메타(상단 표시용) ---
    meta = SceneMeta(
      title="Stack Visualizer",
      complexity="push: O(1), pop: O(1), top: O(1)",
      notes="bottom-aligned stack layout",
    )
    
    # --- HUD 텍스트(상단 좌측) ---
    hud_x = float(self._spec.margin)
    hud_y = float(self._spec.margin)
    
    items.append(
      TextItem(
                key="hud:title",
                pos=Vec2(hud_x, hud_y),
                text=meta.title,
                style=Style(role="hud_title"),
                align="left",
                z=100,
            )
    )
    
    items.append(
      TextItem(
                key="hud:complexity",
                pos=Vec2(hud_x, hud_y + 24.0),
                text=meta.complexity,
                style=Style(role="hud_subtitle"),
                align="left",
                z=100,
            )
    )
    
    # --- Stack Rect + 값 텍스트 ---
    # i=0 bottom → i가 커질수록 top
    
    for i, (v, geom) in enumerate(zip(values, layout.item_geoms)):
      items.append(
            RectItem(
              key=f"stack:item:{i}",
              geom=geom,
              style=Style(role="stack_item"),
              z=10 + i,
            )
      )
      
      cx = geom.pos.x + geom.size.x / 2.0
      cy = geom.pos.y + geom.size.y / 2.0
      items.append(
          TextItem(
              key=f"stack:item:{i}:text",
              pos=Vec2(cx, cy),
              text=str(v),
              style=Style(role="stack_item_text"),
              align="center",
              z=20 + i,
          )
      )
      
    # --- TOP 포인터(라벨 + 화살표) ---
    items.append(
        TextItem(
            key="stack:top:label",
            pos=layout.top_label_pos,
            text="TOP",
            style=Style(role="pointer_label"),
            align="left",
            z=80,
        )
    )
    items.append(
        ArrowItem(
            key="stack:top:arrow",
            start=layout.top_arrow_start,
            end=layout.top_arrow_end,
            style=Style(role="pointer_arrow"),
            head_size=10.0,
            z=70,
        )
    )
    
    return Scene(
        meta=meta,
        width=self._spec.scene_width,
        height=self._spec.scene_height,
        items=tuple(items),
    )