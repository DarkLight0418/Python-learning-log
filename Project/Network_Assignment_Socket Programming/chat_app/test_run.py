from protocol import make_message, encode_message, extract_messages

msg = make_message("chat", "hanjae", "안녕하세요")
data = encode_message(msg)

print(data)

buffer = data.decode("utf-8")
messages, remain = extract_messages(buffer)

print(messages)
print(remain)