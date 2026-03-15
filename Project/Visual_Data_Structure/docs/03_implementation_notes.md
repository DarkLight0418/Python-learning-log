# VDS 구현 메모 초안

## 1. 목적
이 문서는 현재 VDS의 실제 구현 작업을 위한 메모와 리팩토링 방향을 정리한다. 요구사항과 설계 문서에서 확정된 내용을 코드 구조로 옮기는 과정에서 참고한다.

---

## 2. 추천 디렉토리 구조(초안)

```
└── vds/
    ├── app/
    │   ├── controller.py
    │   └── runner.py
    ├── core/
    │   ├── stack.py
    │   └── errors.py
    ├── presenter/
    │   ├── models.py
    │   ├── stack_presenter.py
    │   └── scene_builder.py
    ├── animation/
    │   ├── interpolator.py
    │   └── animator.py
    ├── view/
    │   ├── tk_canvas_view.py
    │   └── draw_registry.py
    └── tests/
        ├── test_stack.py
        ├── test_stack_presenter.py
        └── test_scene_builder.py
```

---

## 3. 파일 역할 메모

### 3.1 core/stack.py
- Stack 상태와 연산 구현
- push/pop/top/is_empty/size/clear/snapshot 담당
- UI 관련 로직 금지

### 3.2 core/errors.py
- EmptyStackError
- 향후 DomainError, ValidationError 확장 가능

### 3.3 presenter/models.py
- Scene, SceneMeta, RectItem, TextItem, ArrowItem 등 정의
- View가 사용하는 공통 출력 모델

### 3.4 presenter/stack_presenter.py
- Stack 상태를 Scene으로 번역
- 연산 결과 강조 정책 연결

### 3.5 presenter/scene_builder.py
- Scene 조립 책임 분리
- Presenter 비대화 방지 목적

### 3.6 view/tk_canvas_view.py
- Tkinter Canvas 렌더링 담당
- Scene만 받아 그림 생성

### 3.7 view/draw_registry.py
- Drawable 타입별 draw 함수/전략 매핑
- if/elif 체인 축소 목적

### 3.8 animation/interpolator.py
- Drawable 간 보간 정책
- 향후 애니메이션 확장 기반

---

## 4. 현재 리팩토링 우선순위

### 우선순위 1
- 도메인 예외를 `errors.py`로 분리
- Stack 순수성 강화
- Scene 출력 계약 점검

### 우선순위 2
- Presenter에서 Scene 조립 책임 분리 여부 검토
- SceneBuilder 도입 시점 판단
- 오류 출력 정책 정리

### 우선순위 3
- View의 draw 로직을 registry 기반으로 전환
- animation 계층 인터페이스 정리
- 테스트 코드 확장

---

## 5. 테스트 관점 메모

### 5.1 core 테스트
- push/pop/top 정상 동작
- 빈 스택 예외
- snapshot 안전 복사

### 5.2 presenter 테스트
- Stack 상태 → Scene 변환 검증
- 연산 후 강조 요소 검증
- 오류 상황 출력 검증

### 5.3 view 테스트
- Scene 입력 시 적절한 draw 함수 호출 여부
- Drawable 타입별 렌더링 매핑 검증

---

## 6. 구현 시 주의점
- 요구사항 문장을 구현 세부로 바로 치환하지 않는다.
- Presenter가 도메인 규칙을 먹어버리지 않도록 한다.
- View가 자료구조별 조건 분기를 갖지 않게 한다.
- Scene 모델은 View 친화적으로, 도메인과는 분리한다.

---

## 7. 이후 작업 후보
- Stack 1차 릴리즈 범위 확정
- Queue/Heap 확장 가능성 검토
- SceneMeta 내용 표준화
- step / scene / sequence 모델 별도 문서화
- 애니메이션 도입 시 인터폴레이션 계약 확정
