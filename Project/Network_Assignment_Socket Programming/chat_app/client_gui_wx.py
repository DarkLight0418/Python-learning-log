"""
client_gui_wx.py

wxPython 기반 채팅 클라이언트 GUI입니다.

실행 전:
    pip install wxPython

실행:
    python client_gui_wx.py

테스트 순서:
1. python server.py
2. python client_gui_wx.py
3. 클라이언트를 하나 더 실행
4. 둘 다 127.0.0.1:5000으로 접속
"""

from __future__ import annotations

import queue
from typing import Any

import wx

from client_network import ChatClientNetwork

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "5000"

class ChatFrame(wx.Frame):
    def __init__(self) -> None:
        super().__init__(
            parent=None,
            title="네트워크 소켓 프로그래밍 채팅 프로그램",
            size=(720, 520),
        )
        
        # 네트워크 수신 메시지를 담을 Queue
        self.inbox: "queue.Queue[dict[str, Any]]" = queue.Queue()
        
        