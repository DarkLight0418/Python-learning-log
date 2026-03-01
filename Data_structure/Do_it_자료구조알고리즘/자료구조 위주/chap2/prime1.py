# 1,000 이하의 소수를 나열하기

counter = 0  # 나눗셈 횟수 카운트

"""
for-else문

반복문이 정상적으로 끝나면 → else 실행
반복문이 break로 중간 종료되면 → else 실행 안 됨

"""
for n in range(2, 1001):
  for i in range(2, n):
    counter += 1
    if n % i == 0:  # 나누어 떨어지면 소수가 아님
      break
  else:
    print(n)
    
print(f'나눗셈을 실행한 횟수: {counter}')