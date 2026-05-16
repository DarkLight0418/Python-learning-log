from __future__ import annotations
import json
from typing import Any

ENCODING = "utf-8"
DELIMITER = "\n"

# 문자열 처리 -> 상수화

# 2026-05-09 수정: @dataclasses 모듈 써서 하는 건줄 알았는데
# 일반 클래스 상수로도 되는구나...
class Type:
  TYPE_JOIN = "join"
  TYPE_CHAT = "chat"
  TYPE_LEAVE = "leave"


def make_message(
    message_type: str,
    sender: str = "system",
    message: str = "",
    *,
    sender_id: str = "",
    display_name: str = "",
    timestamp: str = "",
    ) -> dict[str, Any]:
      data: dict[str, Any] = {
        "type": message_type,
        "sender": sender,
        "message": message,
      }
      
      if sender_id:
        data["sender_id"] = sender_id
      
      if display_name:
        data["display_name"] = display_name
        
      if timestamp:
        data["timestamp"] = timestamp
      
      return data
  
def encode_message(message: dict[str, Any]) -> bytes:
  
  # 방어 코드(오류 발견했을 때 조용히 넘기지 말 것!)
  if not isinstance(message, dict):
    raise TypeError(f"message must be dict, got {type(message).__name__}")
  
  json_text = json.dumps(message, ensure_ascii=False)
  return (json_text + DELIMITER).encode(ENCODING)

def decode_message(line: str) -> dict[str, Any] | None:
  line = line.strip()
  
  if not line:
    return None
  
  try:
    data = json.loads(line)
  except json.JSONDecodeError:
    return None
  
  if not isinstance(data, dict):
    return None
  
  return data

def extract_messages(buffer: str) -> tuple[list[dict[str, Any]], str]:
  messages: list[dict[str, Any]] = []
  while DELIMITER in buffer:
    line, buffer = buffer.split(DELIMITER, 1)
    
    message = decode_message(line)
    
    if message is not None:
      messages.append(message)
      
  return messages, buffer