from __future__ import annotations
import json
from typing import Any

ENCODING = "utf-8"
DELIMITER = "\n"

def make_message(message_type: str, sender: str, message: str) -> dict[str, str]:
  return {
    "type" : message_type,
    "sender" : sender,
    "message" : message,
  }
  
def encode_message(message: dict[str, Any]) -> bytes:
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