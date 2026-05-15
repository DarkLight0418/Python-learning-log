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
        
        # 실제 네트워크 객체
        self.network: ChatClientNetwork | None = None
        
        self.build_ui()
        self.bind_events()
        
        # Queue를 주기적으로 확인할 타이머
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(100)
        
        self.set_connected_state(False)
        
        self.Centre()
        
    def build_ui(self) -> None:
        """
        화면 구성 담당 함수
        """
        
        root = wx.Panel(self)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # ============================
        # 접속 설정 영역
        # ============================
        
        connection_box = wx.StaticBox(root, label="Connection")
        connection_sizer = wx.StaticBoxSizer(connection_box, wx.VERTICAL)
        
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        
        row1.Add(
            wx.StaticText(root, label="Server IP"),
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,
            6,
        )
        
        self.host_input = wx.TextCtrl(root, value=DEFAULT_HOST)
        row1.Add(self.host_input, 1, wx.RIGHT, 12)
        
        row1.Add(
            wx.StaticText(root, label="Port"),
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,
            6,
        )
        
        self.port_input = wx.TextCtrl(root, value=DEFAULT_PORT, size=(90, -1))
        row1.Add(self.port_input, 0, wx.RIGHT, 12)
        
        row1.Add(
            wx.StaticText(root, label="Nickname"),
            0,
            wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,
            6,
        )
        
        self.nickname_input = wx.TextCtrl(root, value="강냉이", size=(130, -1))
        row1.Add(self.nickname_input, 0, wx.RIGHT, 12)
        
        self.connect_button = wx.Button(root, label="Connect")
        row1.Add(self.connect_button, 0)
        
        connection_sizer.Add(row1, 0, wx.EXPAND | wx.ALL, 8)
    
        # ============================
        # 채팅 출력 영역
        # ============================
        self.message_input = wx.TextCtrl(
            root,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2,
        )
        
        # ============================
        # 메시지 입력 영역
        # ============================
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.message_input = wx.TextCtrl(
            root,
            style=wx.TE_PROCESS_ENTER,
        )
        input_sizer.Add(self.message_input, 1, wx.RIGHT, 8)
        
        self.send_button = wx.Button(root, label="Send")
        input_sizer.Add(connection_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(
            self.chat_output,
            1,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10,
        )
        
        root.SetSizer(main_sizer)
    
    def bind_events(self) -> None:
        """
        버튼 클릭, Enter 입력, 창 닫기 이벤트를 연결합니다.
        """
        self.Bind(wx.EVT_BUTTON, self.on_connect_clicked, self.connect_button)
        self.Bind(wx.EVT_BUTTON, self.on_send_clicked, self.send_button)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_send_clicked, self.message_input)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
    def on_connect_clicked(self, event: wx.CommandEvent) -> None:
        """
        Connect 버튼 클릭 시 실행.

        이미 연결되어 있으면 Disconnect 역할을 합니다.
        """
        if self.network is not None and self.network.is_connected:
            self.disconnect()
            return
        
        host = self.host_input.GetValue().strip()
        port_text = self.port_input.GetValue().strip()
        nickname = self.nickname_input.GetValue().strip()
        
        if not host:
            self.append_system_message("서버 IP를 입력하세요.")
            return
        
        if not nickname:
            self.append_system_message("닉네임을 입력하세요.")
            return
        
        try:
            port = int(port_text)
        except ValueError:
            self.append_system_message("포트 번호는 숫자로 입력하세요.")
            return
        self.network = ChatClientNetwork(self.inbox)
        
        try:
            self.network.connect(host, port, nickname)
            
        except OSError as exc:
            self.network = None
            self.append_system_message(f"서버에 접속할 수 없습니다: {exc}")
            self.set_connected_state(False)
            return
        
        self.append_system_message(f"{host}:{port} 서버에 접속했습니다.")
        self.set_connected_state(True)
        self.message_input.SetFocus()
        
    def on_send_clicked(self, event: wx.CommandEvent) -> None:
        """
        Send 버튼 또는 Enter 입력 시 실행됩니다.
        """
        if self.network is None or not self.network.is_connected:
            self.append_system_message("먼저 서버에 접속하세요.")
            return
        
        text = self.message_input.GetValue().strip()
        
        if not text:
            return
        
        try:
            self.network.send_chat(text)
            self.message_input.Clear()
            
        except ConnectionError:
            self.append_system_message("메시지를 보낼 수 없습니다.")
            self.set_connected_state(False)
            
    def on_timer(self, event: wx.TimerEvent) -> None:
        """
        wx.Timer가 주기적으로 호출하는 함수입니다.

        Queue에 쌓인 네트워크 메시지를 꺼내서 GUI에 출력합니다.
        이 함수는 GUI 메인 스레드에서 실행되므로 위젯 수정이 안전합니다.
        """
        while True:
            try:
                message = self.inbox.get_nowait()
            except queue.Empty:
                break
            
            self.append_message(message)
            
            if message.get("type") == "error":
                self.set_connected_state(False)
    
    def append_message(self, message: dict[str, Any]) -> None:
        """
        메시지 type에 따라 출력 형식을 다르게 처리합니다.
        """
        message_type = message.get("type", "")
        sender = message.get("sender", "unknown")
        text = message.get("message", "")
        
        if message_type == "chat":
            self.append_chat_line(f"{sender}: {text}")  
        elif message_type in ("join", "leave"):
            self.append_chat_line(f"* {text}")
        elif message_type == "error":
            self.append_system_message(str(text))            
        else:
            self.append_chat_line(str(message))
            
class ChatApp(wx.App):
    def OnInit(self) -> bool:
        frame = ChatFrame()
        frame.Show()
        return True

if __name__ == "__main__":
    app = ChatApp(False)
    app.MainLoop()