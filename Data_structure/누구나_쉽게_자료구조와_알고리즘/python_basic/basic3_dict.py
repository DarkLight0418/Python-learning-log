item = dict()

print("+++ 딕셔너리를 이용해 게임 아이템 입력 받기 +++")

for i in range(3):
  game_item_name = input("아이템 입력하기 >> ")
  count = int(input("구매할 개수는? >> "))
  item[game_item_name] = count

print("당신이 구매한 아이템은 다음과 같습니다.")
print(item)  
  
print("="*50)
result = input("당신이 확인하고 싶은 아이템은 무엇입니까? >> ")
test = item.get(result)  # key -> value
if result in item:
  print(f'당신이 찾는 {result}은/는 {test}개 있습니다.')
else:
  print(f'당신이 찾는 {result}은/는 없네요...')