"""
1. 클라이언트 접속 받기
2. 클라이언트가 보낸 메시지 받기
3. 모든 클라이언트에게 메시지 뿌리기
"""
from __future__ import annotations

import socket
import threading
from dataclasses import dataclass

from protocol import ENCODING, encode_message, extract_messages, make_message

HOST = "0.0.0.0"
PORT = 5000
RECV_SIZE = 4096

@dataclass
class ClientInfo:
  socket: socket.socket
  address: tuple[str, int]
  nickname: str
  
class ChatServer:
  def __init__(self, host: str = HOST, port: int = PORT) -> None:
    self.host = host
    self.port = port
    
    self.server_socket: socket.socket | None = None

    # key: client socket, value: client information
    self.clients: dict[socket.socket, ClientInfo] = {}
    
    # 여러 스레드가 clients에 접근하므로 Lock 사용
    self.clients_lock = threading.Lock()
    
    self.running = False
    
  def start(self) -> None:
    """
    서버를 시작하고 클라이언트 접속을 계속 기다립니다.
    """
    self.running = True
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
      # 서버를 껐다 켰을 때 포트 재사용을 조금 더 쉽게 해줍니다.
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      
      server_socket.bind((self.host, self.port))
      server_socket.listen()
      
      self.server_socket = server_socket
      
      print(f"[SERVER] Listening on {self.host}:{self.port}")
      
      try:
        while self.running:
          client_socket, address = server_socket.accept()
          
          print(f"[SERVER] 연결됨: {address}")
          
          with self.clients_lock:
            self.clients[client_socket] = ClientInfo(
              socket=client_socket,
              address=address,
              nickname="",
            )
            
          client_thread = threading.Thread(
            target=self.handle_client,
            args=(client_socket,),
            daemon=True,
          )
          client_thread.start()
          
      except KeyboardInterrupt:
        print("\n[SERVER] Ctrl+C 입력, 서버를 종료합니다.")
      
      finally:
        self.stop()
  
  
  def handle_message(self, client_socket: socket.socket, message: dict) -> None:
    """
    _summary_

    Args:
        client_socket (socket.socket): _description_
        message (dict): _description_
    
    클라이언트가 보낸 메시지 타입에 따라 처리합니다.

    """
    
    message_type = message.get("type")
    sender = str(message.get("sender", "unknown"))
    text = str(message.get("message", ""))
    
    if message_type == "join":
      self.set_nickname(client_socket, sender)
      
      join_message = make_message(
        "join",
        sender,
        f"{sender}님이 입장했습니다.",
      )
      self.broadcast(join_message)
        
        
    elif message_type == "chat":
      chat_message = make_message(
        "chat",
        sender,
        text,
      )
      
      self.broadcast(chat_message)
      
    elif message_type == "leave":
      # 직접 브로드캐스트하지 않음, finally의 remove_client(()에서 퇴장 메시지 하나만 보내게 함
      self.remove_client(client_socket, notify_leave=True)
      
      