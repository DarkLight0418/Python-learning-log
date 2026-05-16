"""
1. 클라이언트 접속 받기
2. 클라이언트가 보낸 메시지 받기
3. 모든 클라이언트에게 메시지 뿌리기
"""
from __future__ import annotations

import socket
import threading
from dataclasses import dataclass
from uuid import uuid4

from protocol import ENCODING, encode_message, extract_messages, make_message

HOST = "0.0.0.0"
PORT = 5000
RECV_SIZE = 4096

@dataclass
class ClientInfo:
  socket: socket.socket
  address: tuple[str, int]
  client_id: str
  nickname: str
  display_name: str
  
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
      
      # accept()가 영원히 막히지 않도록 timeout 설정
      server_socket.settimeout(1.0)
      
      self.server_socket = server_socket
      
      print(f"[SERVER] Listening on {self.host}:{self.port} / 서버 종료 Ctrl+C")
      
      try:
        while self.running:
          '''
          내부 try-catch
          -> 1초마다 깨어나서 self.running 상태와 Ctrl+C 확인 
          == accept() 무한정 대기 방지!!
          '''
          try:
            client_socket, address = server_socket.accept()
          except socket.timeout:
            continue
          
          print(f"[SERVER] 연결됨: {address}")
          
          
          # UUID 통해서 일련의 멤버 값 생성하는 거
          client_id = uuid4().hex[:8]
          
          with self.clients_lock:
            self.clients[client_socket] = ClientInfo(
              socket=client_socket,
              address=address,
              client_id=client_id,
              nickname="",
              display_name=f"guest#{client_id[:4]}"
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
  
  def handle_client(self, client_socket: socket.socket) -> None:
    """
    특정 클라이언트로부터 메시지를 계속 수신합니다.
    """
    buffer = ""
    
    try:
      while self.running:
        data = client_socket.recv(RECV_SIZE)
        
        if not data:
          break
        buffer += data.decode(ENCODING)
        
        messages, buffer = extract_messages(buffer)
        
        for message in messages:
          self.handle_message(client_socket, message)
          
    except OSError:
      pass
    
    finally:
      self.remove_client(client_socket, notify_leave=True)
  
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
      
  def set_nickname(self, client_socket: socket.socket, nickname: str) -> ClientInfo | None:
    """ 
    클라이언트 닉네임, 표시 이름 저장
    """
    with self.clients_lock:
      info = self.clients.get(client_socket)
      
      if info is None:
        return None
      info.nickname = nickname
      info.display_name = f"{nickname}#{info.client_id[:4]}"
      
      return info
    
  def broadcast(self, message: dict[str, str]) -> None:
    """
    현재 접속 중인 모든 클라이언트에게 메시지 전송
    """
    with self.clients_lock:
      client_sockets = list(self.clients.keys())
      
    broken_clients: list[socket.socket] = []
    
    for client_socket in client_sockets:
      try:
        client_socket.sendall(encode_message(message))
      except OSError:
        broken_clients.append(client_socket)
    
    for broken_socket in broken_clients:
      self.remove_client(broken_socket, notify_leave=True)
      
  def remove_client(self, client_socket: socket.socket, notify_leave: bool = True) -> None:
    """
    클라이언트 목록에서 제거하고 소켓을 닫습니다.
    """
    
    nickname = ""
    
    with self.clients_lock:
      info = self.clients.pop(client_socket, None)
      
      if info is not None:
        nickname = info.nickname
        
    try:
      client_socket.close()
    except OSError:
      pass
    
    if nickname:
      print(f"[SERVER] 제거됨: {nickname}")
      
      if notify_leave:
        leave_message = make_message(
          "leave",
          nickname,
          f"{nickname}님이 퇴장했습니다.",
        )
        
        self.broadcast(leave_message)
  
  def stop(self) -> None:
    """
    서버와 모든 클라이언트 소켓을 닫습니다.
    """
    self.running = False
    
    with self.clients_lock:
      client_sockets = list(self.clients.keys())
      self.clients.clear()
      
    for client_socket in client_sockets:
      try:
        client_socket.close()
      except OSError:
        pass
      
    if self.server_socket is not None:
      try:
        self.server_socket.close()
      except OSError:
        pass
      
    print("[SERVER] 종료(멈춤)")
    
if __name__ == "__main__":
  server = ChatServer()
  server.start()