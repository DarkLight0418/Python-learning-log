# 배열을 이용한 최댓값
from typing import Any, Sequence
'''
Any == 제약이 없는 임의의 자료형, Sequence == 시퀀스(리스트, 바이트 배열, 문자열, 튜플, 바이트)형
'''
def max_of(a:Sequence) -> Any:
    # 시퀀스형 a 원소의 최댓값 반환 -- 건네받는 매개변수 a의 자료형은 Sequence라는 뜻, 반환하는 것은 임의의 자료형인 Any
    maximum = a[0]
    for i in range(len(a)):
        if a[i] > maximum:
            maximum = a[i]
        return maximum

if __name__ == '__main__':
    print('배열의 최댓값을 구합니다.')
    num = int(input('원소 수를 입력하세요.:'))
    x = [None] * num  # 원소 수가 num인 리스트 생성

    for i in range(num):
        x[i] = int(input(f'x[{i}]값을 입력하세요.:'))
    

    print(f'최댓값은 {max_of(x)}입니다.')
