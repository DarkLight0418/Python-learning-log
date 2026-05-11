"""
client_network.py

클라이언트의 네트워크 기능만 담당하는 파일입니다.

설계 원칙:
- 이 파일은 wxPython을 import하지 않습니다.
- GUI 위젯을 직접 수정하지 않습니다!

# 즉 GUI에 절대 관여하면 안된다는 뜻

- 서버와의 연결, 송신, 수신만 담당합니다.
- 수신한 메시지는 Queue에 넣습니다.
"""
from __future__ import annotations

import queue
import socket
import threading
from typing import Any

from protocol import ENCODING, Type, encode_message, extract_messages, make_message

RECV_SIZE = 4096

class ChatClientNetwork:
  def __init__(self, inbox: "queue.Queue[dict[str, Any]]") -> None:
    self.inbox = inbox
    
    self.sock: socket.socket | None = None
    self.nickname = ""
    
    self.running = threading.Event()
    self.send_lock = threading.Lock()
    
    self.receive_thread: threading.Thread | None = None
    
  