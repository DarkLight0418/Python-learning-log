# 리스트 원소 스캔

x = ['John', 'Messi', 'Ronaldo', 'Frenkie']

# 일반 반복문
print("1번")
for i in range(len(x)):
  print(f'x[{i}] = {x[i]}')
  
print()
print("2번")
# enumerate() 함수
for i, name in enumerate(x):
  print(f'x[{i}] = {name}')
  
print()
print("3번")

# enumerate() 1부터
for i, name in enumerate(x, 1):
  print(f'{i}번째 = {name}')
  
print()
print('4번')

# 인덱스 값 미사용
for i in x:
  print(i)