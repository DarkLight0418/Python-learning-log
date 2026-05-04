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

client = []