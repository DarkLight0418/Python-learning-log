'''
순수 보간 API (Scene Interpolator)

- 정책(MVP):
  - 공통 key만 보간
  - 등장(enter)은 즉시 표시
  - 퇴장(exit)은 즉시 제거 (prev-only는 mid에 포함하지 않음)
  - 보간 불가(타입 다름/핸들러 없음) => next 아이템으로 대체
  
2026.03.04. 최초 작성
'''
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple, Type, TypeVar

from vds.utils.scene_models import (
    Scene,
    RectItem,
    TextItem,
    ArrowItem,
    RectGeom,
    Vec2,
    Drawable,
)

T = TypeVar("T", bound=Drawable)

# -------
# Policy
# -------

@dataclass(frozen=True)
class InterpPolicy:
  """
  Interpolator 동작 규칙.
  - include_entering: next-only 아이템을 mid에 포함할지 (MVP: True)
  - include_exiting: prev-only 아이템을 mid에 포함할지 (MVP: False)
  - interpolate_size: RectGeom.size도 보간할지 (MVP: True/False 선택)
  - sort_keys: deterministic output을 위해 key iteration 정렬 여부
  """
  include_entering: bool = True
  include_exiting: bool = False
  interpolate_size = bool = True
  sort_keys: bool = True
  
DEFAULT_POLICY = InterpPolicy()

# -----------------
# Math helpers
# -----------------

def lerp(a: float, b: float, t: float) -> float:
  return a + (b - a) * t

def lerp_vec2(p: Vec2, q: Vec2, t: float) -> Vec2:
  return Vec2(x=lerp(p.x, q.x, t), y=lerp(p.y, q.y, t))

def lerp_rectgeom(g1: RectGeom, g2: RectGeom, t: float, *, interpolate_size: bool) -> RectGeom:
  if interpolate_size:
    size = Vec2(x=lerp(g1.size.x, g2,size.x, t), y=lerp(g1.size.y, g2.size.y, t))
  else:
    # MVP 안정성: size는 next 기준 고정
    size = g2.size
  return RectGeom(pos=lerp_vec2(g1.pos, g2.pos, t), size=size)

# -------------------------------
# Registry (type-based dispatch)
# -------------------------------

InterpFn = Callable[[Drawable, Drawable, float, InterpPolicy], Drawable]


class InterpRegistry:
  """
  (typeA, typeB) -> handler 로 보간 함수를 등록.
  - 현재는 동일 타입끼리만 등록하는 걸 기본으로 사용.
  """
  def __init__(self) -> None:
      self._handlers: Dict[Tuple[Type[Drawable], Type[Drawable]], InterpFn] = {}

  def register(self, ta: Type[Drawable], tb: Type[Drawable], fn: InterpFn) -> None:
      self._handlers[(ta, tb)] = fn

  def get(self, ta: Type[Drawable], tb: Type[Drawable]) -> Optional[InterpFn]:
      return self._handlers.get((ta, tb))
    
REGISTRY = InterpRegistry()

def _interp_rect(a: Drawable, b: Drawable, t:float, policy: InterpPolicy) -> Drawable:
  assert isinstance(a, RectItem) and isinstance(b, RectItem)
  return RectItem(
    key=a.key,
    geom=lerp_rectgeom(a.geom, b.geom, t, interpolate_size=policy.interpolate_size),
    style=b.style,
    z=b.z,
  )
  
def _interp_text(a: Drawable, b: Drawable, t: float, policy: InterpPolicy) -> Drawable:
  assert isinstance(a, TextItem) and isinstance(b, TextItem)
  return TextItem(
      key=a.key,
      pos=lerp_vec2(a.pos, b.pos, t),
      text=b.text,      # MVP: text는 next 기준
      style=b.style,
      align=b.align,
      z=b.z,
  )
  
def _interp_arrow(a: Drawable, b: Drawable, t: float, policy: InterpPolicy) -> Drawable:
  assert isinstance(a, ArrowItem) and isinstance(b, ArrowItem)
  return ArrowItem(
      key=a.key,
      start=lerp_vec2(a.start, b.start, t),
      end=lerp_vec2(a.end, b.end, t),
      style=b.style,
      head_size=b.head_size,
      z=b.z,
  )
  
REGISTRY.register(RectItem, RectItem, _interp_rect)
REGISTRY.register(TextItem, TextItem, _interp_text)
REGISTRY.register(ArrowItem, ArrowItem, _interp_arrow)

# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------
