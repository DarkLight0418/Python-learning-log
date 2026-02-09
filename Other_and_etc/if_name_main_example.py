def add(a, b):
  return a + b

print("계산기 로딩됨")

'''
if __name__ == "__main__"
  
  이 파일이 직접 실행된 주인공 파일이라면
→ 아래 코드를 실행하고
  남의 파일에서 부품으로 불려온 거라면
→ 실행하지 마!

'''

if __name__ == "__main__":
  print(add(2, 3))