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
  
  
  def handle_message(self, client_socket: socket.socket, message: dict) -> None:
    """
    _summary_

    Args:
        client_socket (socket.socket): _description_
        message (dict): _description_
    
    클라이언트가 보낸 메시지 타입에 따라 처리합니다.

    """