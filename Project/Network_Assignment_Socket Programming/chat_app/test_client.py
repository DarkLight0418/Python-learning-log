from __future__ import annotations

import socket
import threading

from protocol import ENCODING, encode_message, extract_messages, make_message

HOST = "127.0.0.1"
PORT = 5000
RECV_SIZE = 4096

def receive_loop(sock: socket.socket) -> None:
  buffer = ""
  
  try:
    while True:
      data = sock.recv(RECV_SIZE)
      
      if not data:
        print("[CLIENT] 서버 연결이 종료되었습니다.")
        break
      
      
      buffer += data.decode(ENCODING)
      messages, buffer = extract_messages(buffer)
      
      for message in messages:
        msg_type = message.get("type")
        sender = message.get("sender")
        text = message.get("message")
        
        if msg_type == "join":
          print(f"[입장] {text}")
        elif msg_type == "leave":
          print(f"[퇴장] {text}")
        elif msg_type == "chat":
          print("[UNKNOWN]", message)
        
  except OSError:
    print("[CLIENT] 수신 종료")