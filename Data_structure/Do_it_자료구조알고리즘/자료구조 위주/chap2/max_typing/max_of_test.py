# 각 배열 원소 최댓값 구해서 출력 (튜플, 문자열, 문자열 리스트)

from max import max_of

t = (4, 7, 5.6, 2, 3.14, 1)
s = 'string'
a = ['DTS', 'AAC', 'FLAC']

print(f'{t}의 최댓값은 {max_of(t)}입니다.')  # 숫자 크기 (수학적 크기)
print(f'{s}의 최댓값은 {max_of(s)}입니다.')  # ASCII 순서 (문자 코드 값)
print(f'{a}의 최댓값은 {max_of(a)}입니다.')  # 첫 글자부터 비교 (사전식)