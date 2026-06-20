"""
StackPanel.

스택 시각화 기능 하나를 담당하는 Tkinter 화면 조각.
MainWindow는 이 클래스를 가져와 배치만 하고,
StackUsecase/Presenter/View 연결은 StackPanel 내부에서 처리.

2026.06.18. 최초 작성
"""

from __future__ import annotations

import tkinter as tk

from vds.presenter.stack_presenter import StackPresenter
from vds.usecases.operations import OperationResult
from vds.usecases.stack_usecase import StackUsecase
from vds.view.tk.canvas_view import TkCanvasView

class StackPanel(tk.Frame):
    """
    Stack 기능 전용 UI 모듈.

    책임:
        - Entry/Button/Canvas 배치
        - 버튼 이벤트 처리
        - StackUsecase 호출
        - Presenter/View를 이용한 화면 갱신

    책임이 아닌 것:
        - root window 생성
        - 앱 전체 메뉴/라우팅 관리
        - 다른 자료구조 화면 관리
    """
    
    def __init__(
        self,
        master: tk.Misc,
        usecase: StackUsecase | None = None,
        presenter: StackPresenter | None = None,
    ):
        super().__init__(master)
        
        self.usecase = usecase or StackUsecase()
        self.presenter = presenter or StackPresenter()
        
        self._build_widgets()
        self._render_current_stack()
        
    def _build_widgets(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.control_frame = tk.Frame(self)
        self.control_frame.grid(row=0, column=0, sticky="ns", padx=12, pady=12)
        
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)
        self.view = TkCanvasView(self.canvas)
        
        title_label = tk.Label(
            self.control_frame,
            text="Stack",
            font=("Arial", 14, "bold"),
            anchor="w",
        )
        
        title_label.pack(fill=tk.x, pady=(0, 12))
        
        self.value_entry = tk.Entry(self.control_frame)
        self.value_entry.pack(fill=tk.X, pady=(0, 8))
        self.value_entry.bind("<Return>", lambda _event: self._handle_push())
        
        self.push_button = tk.Button(
            self.control_frame,
            text="Push",
            command=self._handle_push,
        )
        self.push_button.pack(fill=tk.x, pady=4)
        
        self.pop_button = tk.Button(
            self.control_frame,
            text="Pop",
            command=self._handle_pop,
        )
        self.pop_button.pack(fill=tk.X, pady=4)
        
        self.top_button = tk.Button(
            self.control_frame,
            text="Top",
            command=self._handle_top,
        )
        self.top_button.pack(fill=tk.X, pady=4)
        
        self.clear_button = tk.Button(
            self.control_frame,
            text="Clear",
            command=self._handle_clear,
        )
        self.clear_button.pack(fill=tk.x, pady=4)
        
        self.message_label = tk.Label(
            self.control_frame,
            text="값을 입력하고 Push를 눌러보세요",
            anchor="w",
            justify="left",
            wraplength=180,
        )
        
        self.message_label.pack(fill=tk.x, pady=(16, 0))
        
    def _handle_push(self) -> None:
        result = self.usecase.push(self.value_entry.get())
        if result.ok:
            self.value_entry.delete(0, tk.END)
        self._apply_result(result)