from __future__ import annotations

import socket
import threading

from protocol import ENCODING, TYPE_JOIN, TYPE_CHAT, TYPE_LEAVE, encode_message, extract_messages, make_message

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
        
        if msg_type == TYPE_JOIN:
          print(f"[입장] {text}")
        elif msg_type == TYPE_LEAVE:
          print(f"[퇴장] {text}")
        elif msg_type == TYPE_CHAT:
          print(f"{sender}: {text}")
        else:
          print("[UNKNOWN]", message)
        
  except OSError:
    print("[CLIENT] 수신 종료")
    
    
def main() -> None:
  nickname = input("닉네임 입력: ").strip()
  
  if not nickname:
    print("닉네임은 비워둘 수 없어요...")
    return

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    
    join_message = make_message("join", nickname, "")
    sock.sendall(encode_message(join_message))
    
    thread = threading.Thread(
      target=receive_loop,
      args=(sock,),
      daemon=True,
    )
    thread.start()
    
    print("메시지를 입력하세요. 종료를 원하시면 /q 입력")
    
    while True:
      text = input()
      
      if text == "/q":
        leave_message = make_message("leave", nickname, "")
        sock.sendall(encode_message(leave_message))
        break
      
      if not text.strip():
        continue
      
      chat_message = make_message("chat", nickname, text)
      sock.sendall(encode_message(chat_message))
      
if __name__ == "__main__":
  main()