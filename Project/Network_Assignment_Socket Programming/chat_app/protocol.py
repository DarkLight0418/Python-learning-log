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