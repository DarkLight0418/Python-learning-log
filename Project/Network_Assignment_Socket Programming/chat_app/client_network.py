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
    
  @property
  def is_connected(self) -> bool:
    return self.sock is not None and self.running.is_set()
  
  def connect(self, host: str, port: int, nickname: str) -> None:
    """
    서버 접속 후 수신 스레드 시작
    """
    
    if self.is_connected:
      return
    
    self.nickname = nickname
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # recv에서 영원히 멈추지 않도록 timeout 설정
    sock.settimeout(1.0)
    
    sock.connect((host, port))
    
    self.sock = sock
    self.running.set()
    
    self.receive_thread = threading.Thread(
      target=self.receive_loop,
      daemon=True,
    )
    self.receive_thread.start()
    
    # 서버에게 입장 메시지 전송
    self.send_raw(
      make_message(
        "join",
        self.nickname,
        "",
      )
    )
  def send_raw(self, message: dict[str, Any]) -> None:
    """
    실제 socket.sendall()을 수행합니다.
    여러 곳에서 동시에 send할 가능성을 막기 위해 Lock을 사용합니다.
    """
    if self.sock is None:
      raise ConnectionError("소켓이 연결되지 않았습니다.")
    
    try:
      with self.send_lock:
        self.sock.sendall(encode_message(message))
        
    except OSError as exc:
      self.inbox.put(
        {
          "type": "error",
          "sender": "system",
          "message": "메시지 전송에 실패했습니다.",
        }
      )
      self.close(send_leave=False)
      raise ConnectionError("메시지 전송에 실패했습니다! 확인 바랍니다.") from exc
    
  def receive_loop(self) -> None:
    """
    서버에서 오는 메시지를 계속 수신하는 백그라운드 스레드 함수입니다.
    받은 메시지를 inbox Queue에 넣기만 하도록 코드 짤 것!
    """
    
    buffer = ""
    
    while self.running.is_set():
      if self.sock is None:
        break
      
      try:
        chunk = self.sock.recv(RECV_SIZE)
        
        if not chunk:
          self.inbox.put(
            {
            "type": "error",
            "sender": "system",
            "message": "서버와의 연결이 끊어졌습니다.",
            }
          )
          break
        
        buffer += chunk.decode(ENCODING)
        
        messages, buffer = extract_messages(buffer)
        
        for message in messages:
          self.inbox.put(message)
        
      except socket.timeout:
        # 주기적으로 running 상태 확인을 위한 장치
        continue
      
      except OSError:
        break
      
    self.running.clear()
  
  
  def close(self, send_leave: bool = True) -> None:
    """
    서버 연결을 종료합니다.
    """
    if self.sock is None:
      self.running.clear()
      return
    
    if send_leave and self.running.is_set():
      try:
        leave_message = make_message(
          "leave",
          self.nickname,
          "",
        )
        self.send_raw(leave_message)
        
      except ConnectionError:
        pass
      
    self.running.clear()
    
    try:
      self.sock.shutdown(socket.SHUT_RDWR)
    except OSError:
      pass
    
    try:
      self.sock.close()
    except OSError:
      pass
    
    try:
      self.sock.close()
    except OSError:
      pass
    
    self.sock = None
    