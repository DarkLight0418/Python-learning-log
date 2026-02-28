# 리스트에서 임의의 원솟값을 업데이트

def change(lst, idx, val):
  """ lst[idx]의 값을 val로 업데이트 """
  lst[idx] = val
  
  
x = [11, 22, 33, 44, 55]
print('x = ', x)


index = int(input('업데이트할 인덱스를 선택하세요.: '))
value = int(input('새로운 값을 입력하세요.: '))

change(x, index, value)
print(f'x = {x}')


"""
인수가 뮤터블(변경이 가능한 객체)일 경우 변수 값 변경 시 객체 자체를 업데이트

참조에 의한 호출
"""