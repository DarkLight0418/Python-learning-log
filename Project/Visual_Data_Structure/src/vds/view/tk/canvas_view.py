"""
Tkinter Canvas View
- Presenter가 만든 Scene/Drawable을 Tkinter Canvas에 렌더링함.
- 자료구조 종류(스택/큐/리스트/힙)는 전혀 모름. Scene만 알고 있으니 참고.

2026.02.25 작성
"""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from vds.presenter.models import (
    Scene,
    RectItem,
    TextItem,
    ArrowItem,
    Style,
)

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