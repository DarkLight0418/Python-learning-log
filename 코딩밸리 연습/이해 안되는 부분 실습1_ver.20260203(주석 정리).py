# 금지어 목록
FORBIDDEN_WORDS = ["세일", "판매", "특가", "할인"]

# 검사할 게시글 목록
POST_CONTENTS = [
    "신상 초특가 세일 중",
    "질럿은 야마토 한방에 안죽어",
    "최신 게임 무료 다운 월정액 70%할인 중"
]


def find_forbidden_words(content: str) -> list[tuple[str, int]]:
    """
    게시글 내용에서 금지어와 등장 위치를 찾아 반환한다.
    반환값: [(금지어, 시작 인덱스), ...]
    """
    results = []

    for i in range(len(content)):
        for word in FORBIDDEN_WORDS:
            if content[i:i + len(word)] == word:
                results.append((word, i))

    return results


for content in POST_CONTENTS:
    print(content)

    forbidden_matches = find_forbidden_words(content)

    if forbidden_matches:
        for word, index in forbidden_matches:
            print(f'- "{word}" 금지어가 {index + 1}번째 글자에 등장하니 수정해주세요.')
    else:
        print("글이 성공적으로 등록되었습니다.")

    print()
