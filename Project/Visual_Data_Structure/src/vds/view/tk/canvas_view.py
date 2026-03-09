"""
Tkinter Canvas View
- Presenter가 만든 Scene/Drawable을 Tkinter Canvas에 렌더링함.
- 자료구조 종류(스택/큐/리스트/힙)는 전혀 모름. Scene만 알고 있으니 참고.
-> 나중에 Presenter가 Scene을 만들어주는 구조

2026.02.25 최초 작성
"""

from __future__ import annotations
import tkinter as tk
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from theme import RoleTheme
from Project.Visual_Data_Structure.src.vds.scene.scene_models import (
    Scene,
    RectItem,
    TextItem,
    ArrowItem,
    Style,
)


class TkCanvasView:
  """
  Scene을 통째로 clear -> redraw 하는 단순 렌더링 버전(MVP).
  추후 animator에서 key 기반으로 부분 업데이트를 하더라도,
  여기의 draw_xxx 메서드는 그대로 재사용할 수 있게 설계.
  """
  
  def __init__(self, canvas: tk.Canvas):
    self.canvas = canvas
    self._item_ids_by_key: Dict[str, int] = {}  # key -> canvas item id
    self._last_scene: Optional[Scene] = None
    
    # role 기반 기본 테마(최소 세트)
    self._themes: Dict[str, RoleTheme] = {
        "default": RoleTheme(),
        "rect": RoleTheme(rect_fill="", rect_outline="black"),
        "text": RoleTheme(text_color="black"),
        "arrow": RoleTheme(),

        # 프로젝트에서 자주 쓰는 role들 (theme.py로 분리할 수 있으니 참고할 것.)
        "stack_item": RoleTheme(rect_fill="", rect_outline="black"),
        "stack_item_text": RoleTheme(text_color="black"),
        "hud_title": RoleTheme(text_color="black"),
        "hud_subtitle": RoleTheme(text_color="black"),
        "pointer_label": RoleTheme(text_color="black"),
        "pointer_arrow": RoleTheme(),
    }
    
  # ----------------------------
  # Public API
  # ----------------------------
  def render(self, scene: Scene) -> None:
    """
    MVP: 매 프레임 전체를 지우고 다시 그림.
    추후 성능/애니메이션 최적화 시 key 기반 diff로 바꿀 수 있음.
    """
    self._apply_scene_size(scene)
    self.clear()
    self._draw_scene(scene)
    self._last_scene = scene

  def clear(self) -> None:
    self.canvas.delete("all")
    self._item_ids_by_key.clear()

  def set_theme(self, role: str, theme: RoleTheme) -> None:
    self._themes[role] = theme

  # ----------------------------
  # Internal
  # ----------------------------
  def _apply_scene_size(self, scene: Scene) -> None:
    # Canvas 크기를 Scene에 맞추고 싶으면 활성화
    self.canvas.config(width=scene.width, height=scene.height)
    
  def _draw_scene(self, scene: Scene) -> None:
    for drawable in scene.sorted_items():
      if isinstance(drawable, RectItem):
        item_id = self._draw_rect(drawable)
      elif isinstance(drawable, TextItem):
        item_id = self._draw_text(drawable)
      elif isinstance(drawable, ArrowItem):
        item_id = self._draw_arrow(drawable)
      else:
        continue
      
      self._item_ids_by_key[getattr(drawable, "key")] = item_id
      
  # ----------------------------
  # Drawing primitives
  # ----------------------------
  def _resolve_colors(self, style: Style) -> Tuple[str, str, str]:
    """
    (fill, outline, text) 결정 규칙:
    1) Style에 명시된 값 우선
    2) 없으면 role 테마 기본값 사용
    3) role도 없으면 default 사용
    """
    
    theme = self._themes.get(style.role) or self._themes["default"]
    
    fill = style.fill if style.fill is not None else theme.rect_fill
    outline = style.outline if style.outline is not None else theme.rect_outline
    text = style.text if style.text is not None else theme.text_color
    
    return fill, outline, text
  
  def _dash_pattern(self, style: Style) -> Optional[Tuple[int, int]]:
    if style.stroke.dashed:
      return (6, 4)
    return None
  
  def _draw_rect(self, it: RectItem) -> int:
    fill, outline, _ = self._resolve_colors(it.style)
    dash = self._dash_pattern(it.style)
    
    x1 = it.geom.pos.x
    y1 = it.geom.pos.y
    x2 = it.geom.pos.x + it.geom.size.x
    y2 = it.geom.pos.y + it.geom.size.y
    
    return self.canvas.create_rectangle(
      x1, y1, x2, y2,
      fill=fill,
      outline=outline,
      width=it.style.stroke.width,
      dash=dash
    )

  def _draw_text(self, it: TextItem) -> int:
    _, _, text_color = self._resolve_colors(it.style)
    
    # Tkinter anchor 매핑
    if it.align == "left":
      anchor = "w"
    elif it.align =="right":
      anchor ="e"
    else:
      anchor = "center"
      
    return self.canvas.create_text(
      it.pos.x, it.pos.y,
      text=it.text,
      fill=text_color,
      anchor=anchor
    )
    
  def _draw_arrow(self, it: ArrowItem) -> int:
    fill, outline, _ = self._resolve_colors(it.style)
    dash = self._dash_pattern(it.style)

    # Tkinter line color는 fill 옵션이 핵심(outline 개념이 없음)
    line_color = outline if outline else fill

    # arrowshape ==> (head_length, head_width, neck_width)
    
    hs = max(1.0, float(it.head_size))
    arrowshape = (hs, hs, max(1.0, hs * 0.35))

    return self.canvas.create_line(
        it.start.x, it.start.y, it.end.x, it.end.y,
        fill=line_color,
        width=it.style.stroke.width,
        dash=dash,
        arrow=tk.LAST,
        arrowshape=arrowshape
    )