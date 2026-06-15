# Visual Data Structure 프로젝트 기획서

> 문서 목적: 이 문서는 Visual Data Structure(VDS)의 **프로젝트 방향, 문제 정의, 사용자 가치, MVP 범위, 개발 우선순위**를 고정하기 위한 기준 문서이다.  
> 요구사항 명세(`01_requirements.md`), 아키텍처 문서(`02_architecture.md`), 구현 메모(`03_implementation_notes.md`)보다 앞에서 프로젝트의 중심축을 잡는 역할을 한다.

---

## 1. 프로젝트 개요

**Visual Data Structure(VDS)**는 자료구조의 연산 과정을 시각적으로 보여주는 Python 기반 학습 도구이다.

자료구조를 처음 배우는 사용자는 `push`, `pop`, `top` 같은 연산이 내부 상태를 어떻게 변화시키는지 머릿속으로만 이해해야 하는 경우가 많다. VDS는 이러한 상태 변화를 **Scene 프레임** 단위로 표현하여 사용자가 자료구조의 동작을 단계별로 관찰할 수 있도록 한다.

초기 버전은 **Stack 시각화**를 중심으로 구현하며, 이후 Queue, List, Heap 등 다른 자료구조로 확장할 수 있는 구조를 목표로 한다.

### 1.1 한 줄 정의

> VDS는 자료구조의 연산 결과를 Scene 단위로 시각화하여, 학습자가 상태 변화를 단계적으로 이해할 수 있도록 돕는 Python 기반 학습 도구이다.

### 1.2 현재 단계의 핵심 방향

현재 단계에서 VDS는 완성형 교육 플랫폼이 아니라, **Stack 하나를 제대로 시각화하는 MVP**를 우선 완성하는 프로젝트로 정의한다.

따라서 초기 개발의 기준은 다음과 같다.

- 자료구조 전체를 한 번에 다루지 않는다.
- 복잡한 애니메이션 엔진을 먼저 만들지 않는다.
- GUI 완성도보다 Core → Presenter → Scene → View 흐름의 안정성을 우선한다.
- Stack 연산 결과가 실제 화면에 일관되게 표시되는 것을 1차 목표로 삼는다.

---

## 2. 문제 정의

자료구조 학습에서 초보자가 겪는 어려움은 단순히 문법을 모르는 것이 아니라, **연산 전후의 상태 변화를 머릿속으로 추적하기 어렵다는 점**이다.

예를 들어 Stack에서 다음 연산을 실행한다고 가정한다.

```text
push(10)
push(20)
pop()
top()
```

초보자는 다음 내용을 동시에 이해해야 한다.

- 어떤 값이 Stack에 추가되는가?
- 어느 위치가 최상단인가?
- `pop()` 이후 어떤 값이 제거되는가?
- `top()`은 값을 제거하지 않는다는 점을 어떻게 확인할 수 있는가?
- 현재 Stack의 상태는 무엇인가?

교재의 정적인 그림이나 콘솔 출력만으로는 이러한 상태 변화를 직관적으로 이해하기 어렵다. VDS는 이 문제를 해결하기 위해 각 연산 이후의 상태를 **시각적 장면(Scene)**으로 변환한다.

---

## 3. 기존 학습 방식의 한계

| 학습 방식 | 장점 | 한계 |
|---|---|---|
| 교재 그림 | 개념 설명이 정리되어 있음 | 정적인 예시라 연산 흐름을 따라가기 어려움 |
| 콘솔 출력 | 구현이 간단함 | 자료구조의 위치, 방향, 상태 변화가 직관적이지 않음 |
| 디버거 사용 | 실제 코드 흐름 확인 가능 | 초보자에게 진입 장벽이 높음 |
| 온라인 시각화 도구 | 시각적으로 이해하기 쉬움 | 직접 구현한 자료구조 코드와 연결하기 어려움 |

VDS는 이 중에서 **직접 구현한 자료구조 연산 결과를 Scene으로 변환하는 학습 도구**라는 위치를 가진다.

---

## 4. 프로젝트 목표

VDS의 목표는 다음과 같다.

| 목표 | 설명 |
|---|---|
| 자료구조 상태 변화 시각화 | Stack 연산 결과를 화면에 시각적으로 표시한다. |
| 단계별 학습 지원 | 사용자가 한 연산씩 실행하며 상태 변화를 확인할 수 있게 한다. |
| Scene 기반 출력 구조 확립 | View가 자료구조 내부를 몰라도 Scene만 보고 렌더링할 수 있게 한다. |
| 테스트 가능한 구조 유지 | GUI 없이도 Core와 Presenter를 검증할 수 있게 한다. |
| 확장 가능한 기반 마련 | Stack 이후 Queue, List, Heap 등으로 확장할 수 있는 구조를 준비한다. |

### 4.1 1차 목표

> Stack 연산을 실행하면, 그 결과가 Scene으로 만들어지고, View가 그 Scene을 화면에 그릴 수 있어야 한다.

### 4.2 1차 목표가 아닌 것

현재 단계에서 다음 항목은 핵심 목표가 아니다.

- 모든 자료구조 지원
- 고급 애니메이션 엔진 구현
- 완성도 높은 디자인 시스템 구축
- 사용자 계정, 저장, 기록 관리 기능
- 웹/모바일 서비스화
- 알고리즘 전체 시각화 플랫폼화

---

## 5. 주요 사용자

초기 VDS의 사용자는 넓게 잡지 않는다. MVP 단계에서는 다음 사용자를 기준으로 한다.

| 사용자 | 설명 | 기대 가치 |
|---|---|---|
| 자료구조 입문자 | Stack의 동작 과정을 눈으로 확인하고 싶은 학습자 | 연산 전후 상태 변화를 쉽게 이해한다. |
| Python 학습자 | 자료구조와 GUI 구조를 함께 공부하는 개발자 | 자료구조 구현과 시각화 구조를 함께 학습한다. |
| 프로젝트 개발자 | 설계, 테스트, 시각화 구조를 훈련하는 개발자 | Core, Presenter, View 분리 경험을 얻는다. |

---

## 6. 핵심 가치

VDS가 제공해야 하는 핵심 가치는 세 가지이다.

### 6.1 보이는 자료구조

자료구조의 내부 상태를 텍스트가 아니라 도형으로 보여준다.

예시:

```text
push(10)

Before: []
After:  [10]
```

이 결과를 단순 텍스트가 아니라 Stack 박스 형태로 표현한다.

### 6.2 단계별 이해

사용자는 최종 결과만 보는 것이 아니라, 연산 단위로 상태 변화를 확인한다.

```text
1단계: push(10)
2단계: push(20)
3단계: top()
4단계: pop()
```

각 단계는 Scene으로 변환되며, 사용자는 현재 자료구조 상태를 시각적으로 확인할 수 있다.

### 6.3 확장 가능한 시각화 구조

초기에는 Stack만 구현하지만, 구조는 다음과 같이 확장 가능해야 한다.

```text
Stack  → StackPresenter  → Scene → View
Queue  → QueuePresenter  → Scene → View
List   → ListPresenter   → Scene → View
Heap   → HeapPresenter   → Scene → View
```

View는 Stack, Queue, List의 내부 구현을 직접 알지 않는다. View는 오직 Scene을 렌더링한다.

---

## 7. MVP 범위

### 7.1 MVP 이름

**Stack Visualizer MVP**

### 7.2 MVP 목표

값을 입력하고 `push` 버튼을 누르면 Stack에 값이 쌓이고, `pop` 버튼을 누르면 최상단 값이 제거되며, 그 결과가 Canvas에 표시되는 상태를 만든다.

### 7.3 MVP 포함 범위

| 구분 | 포함 내용 |
|---|---|
| 자료구조 | Stack |
| 연산 | push(value), pop(), top(), clear() |
| 출력 | 현재 Stack 상태 Scene |
| GUI | 입력창, push/pop/top/clear 버튼, Canvas, 메시지 영역 |
| 오류 처리 | 빈 Stack에서 pop/top 시 오류 메시지 표시 |
| 테스트 | Stack Core 테스트, StackPresenter 테스트 |
| 구조 | Core → Presenter → Scene → View 흐름 유지 |

### 7.4 MVP 제외 범위

| 제외 항목 | 제외 이유 |
|---|---|
| Queue/List/Heap 동시 구현 | Stack 완성 전 범위가 과도하게 커짐 |
| 복잡한 애니메이션 엔진 | Scene 구조 안정화 이후 도입하는 것이 적절함 |
| 저장/불러오기 | 핵심 학습 흐름과 직접 관련이 낮음 |
| 사용자 계정/학습 기록 | 개인 학습 도구 MVP 범위를 넘어섬 |
| 웹/모바일 지원 | Tkinter MVP 완성 이후 판단할 사항 |
| 고급 알고리즘 시각화 | 자료구조 단일 연산 시각화부터 완성해야 함 |

---

## 8. 주요 기능

### FR-01. Stack 값 추가

사용자는 입력창에 값을 입력하고 `push` 버튼을 눌러 Stack에 값을 추가할 수 있다.

```text
입력: 10
동작: push
결과: Stack 상단에 10 추가
```

### FR-02. Stack 값 제거

사용자는 `pop` 버튼을 눌러 Stack의 최상단 값을 제거할 수 있다.

```text
Before: [10, 20, 30]
pop()
After:  [10, 20]
Removed: 30
```

### FR-03. 최상단 값 확인

사용자는 `top` 버튼을 눌러 Stack의 최상단 값을 확인할 수 있다. 이때 Stack의 상태는 변경되지 않는다.

```text
Before: [10, 20, 30]
top()
Result: 30
After:  [10, 20, 30]
```

### FR-04. Stack 초기화

사용자는 `clear` 버튼을 눌러 Stack의 모든 값을 제거할 수 있다.

### FR-05. Scene 생성

각 연산 후 시스템은 현재 Stack 상태를 기반으로 Scene을 생성한다.

Scene은 View가 화면에 그릴 수 있는 출력 계약이다. Scene에는 다음 정보가 포함될 수 있다.

| 항목 | 설명 |
|---|---|
| RectItem | Stack의 각 요소 박스 |
| TextItem | 요소 값, 제목, 설명 |
| ArrowItem | TOP 포인터 |
| SceneMeta | 제목, 시간복잡도, 설명 |

### FR-06. Scene 렌더링

View는 Scene을 받아 Canvas에 렌더링한다.

올바른 방향:

```text
Stack → Presenter → Scene → View
```

피해야 할 방향:

```text
View → Stack 내부 직접 접근 → Canvas에 직접 그림
```

### FR-07. 오류 표시

빈 Stack에서 `pop()` 또는 `top()`을 실행하면 오류를 명확히 보여준다.

예시:

```text
현재 Stack이 비어 있어 pop을 실행할 수 없습니다.
```

MVP 단계에서는 오류 Scene까지 만들지 않아도 된다. 우선 Label 또는 메시지 영역에 오류를 표시하는 방식으로 충분하다.

---

## 9. 사용자 시나리오

### 9.1 기본 시나리오

```text
1. 사용자가 프로그램을 실행한다.
2. 화면에 빈 Stack이 표시된다.
3. 사용자가 입력창에 10을 입력한다.
4. push 버튼을 누른다.
5. Stack에 10이 추가된 Scene이 Canvas에 표시된다.
6. 사용자가 20을 입력하고 push 버튼을 누른다.
7. Stack에 20이 최상단으로 추가된다.
8. 사용자가 pop 버튼을 누른다.
9. 최상단 값 20이 제거되고, Stack에는 10만 남는다.
```

### 9.2 top 확인 시나리오

```text
1. Stack에 10, 20, 30이 들어 있다.
2. 사용자가 top 버튼을 누른다.
3. 시스템은 30이 최상단 값임을 표시한다.
4. Stack 상태는 [10, 20, 30]으로 유지된다.
```

### 9.3 오류 시나리오

```text
1. 사용자가 빈 Stack 상태에서 pop 버튼을 누른다.
2. Core는 EmptyStackError를 발생시킨다.
3. App 또는 Presenter는 오류 메시지를 사용자에게 보여준다.
4. Stack 상태는 변경되지 않는다.
```

---

## 10. 핵심 개념 모델

초기 단계에서는 다음 5개 개념을 중심으로 생각한다.

| 개념 | 역할 |
|---|---|
| Stack | 실제 자료구조 상태와 연산 규칙을 담당한다. |
| Operation | push, pop, top, clear 같은 사용자 요청을 의미한다. |
| Presenter | Stack 상태를 Scene으로 변환한다. |
| Scene | View가 그릴 수 있는 장면 데이터이다. |
| View | Scene을 화면에 렌더링한다. |

### 10.1 현재 단계에서 뒤로 미룰 개념

다음 개념은 중요하지만 MVP의 중심이 아니다.

- Step
- Sequence
- SceneHistory
- AnimationEngine
- Interpolator
- Replay Controller

이 개념들은 Stack 정적 시각화 MVP가 안정화된 이후 확장 단계에서 다룬다.

---

## 11. 설계 방향

### 11.1 기본 데이터 흐름

```text
사용자 입력
→ App/Runner
→ Core(Stack 연산)
→ Presenter(Scene 생성)
→ View(Scene 렌더링)
```

### 11.2 책임 분리 원칙

| 계층 | 책임 | 하지 말아야 할 일 |
|---|---|---|
| Core | 자료구조 상태와 연산 규칙 관리 | UI, 좌표, 색상 처리 |
| Presenter | Core 상태를 Scene으로 변환 | 실제 Canvas 그리기, 자료구조 규칙 구현 |
| Scene | View가 렌더링할 수 있는 출력 데이터 제공 | 도메인 연산 수행 |
| View | Scene을 화면에 그림 | Stack 내부 직접 접근 |
| App/Runner | 입력 흐름 조립 | Core 규칙을 대신 판단 |

### 11.3 Scene 위치에 대한 권장 방향

VDS에서 Scene은 Presenter와 View가 공유하는 핵심 출력 계약이다. 따라서 장기적으로는 `presenter` 내부 모델이라기보다 별도 계층으로 분리하는 것이 자연스럽다.

권장 구조:

```text
vds/
  core/
  scene/
    scene_models.py
  presenter/
  view/
  app/
```

다만 MVP 단계에서는 무리한 파일 이동보다, 먼저 import 기준과 Scene 사용 규칙을 안정화하는 것을 우선한다.

---

## 12. 개발 우선순위

### Phase 1. Stack 정적 시각화 MVP

목표:

> Stack 상태를 Canvas에 안정적으로 보여준다.

작업 항목:

- import 기준 통일
- Stack Core 테스트 통과
- Scene 모델 위치와 사용 규칙 확정
- StackPresenter의 Scene 생성 안정화
- TkCanvasView의 Scene 렌더링 안정화
- push/pop/top/clear 버튼 연결
- 빈 Stack 오류 메시지 표시

완료 기준:

```text
입력창에 10 입력 → push 클릭 → Canvas에 10 박스 표시
pop 클릭 → 박스 제거
빈 상태 pop 클릭 → 오류 메시지 표시
```

### Phase 2. 실행 흐름 정리

목표:

> GUI 입력과 테스트 시뮬레이터가 같은 실행 흐름을 쓰게 한다.

도입 후보:

- Operation
- Runner
- OperationResult
- ErrorResult

### Phase 3. Step/Scene 기록

목표:

> 연산 기록을 남기고, 이전/다음 단계 이동이 가능하게 한다.

도입 후보:

- Step
- SceneHistory
- SceneSequence
- Previous / Next 버튼
- Replay 기능

### Phase 4. 애니메이션

목표:

> Scene과 Scene 사이를 부드럽게 연결한다.

도입 후보:

- AnimationEngine
- Interpolator
- Drawable key 기반 diff
- Scene transition

---

## 13. 성공 기준

MVP 성공 기준은 다음과 같다.

| 기준 | 설명 |
|---|---|
| 기능 성공 | Stack의 push/pop/top/clear가 GUI에서 동작한다. |
| 시각화 성공 | 각 연산 후 Stack 상태가 Canvas에 표시된다. |
| 구조 성공 | View가 Stack 객체를 직접 알지 않고 Scene만 렌더링한다. |
| 테스트 성공 | Core와 Presenter 테스트가 GUI 없이 실행 가능하다. |
| 오류 처리 성공 | 빈 Stack에서 pop/top 시 사용자에게 명확한 실패 메시지를 보여준다. |
| 확장 준비 | Queue/List 추가 시 View 전체를 갈아엎지 않아도 되는 구조를 유지한다. |

---

## 14. 리스크와 대응 전략

| 리스크 | 설명 | 대응 전략 |
|---|---|---|
| 범위 확장 | Stack 완성 전 Queue/List/Animation을 동시에 구현하려는 위험 | MVP 범위를 Stack으로 고정한다. |
| 설계 과잉 | Step, Sequence, Animation을 너무 빨리 도입하는 위험 | 정적 Scene 렌더링 이후 단계적으로 확장한다. |
| View와 Core 결합 | Canvas 코드가 Stack 내부를 직접 참조하는 위험 | Scene을 유일한 렌더링 입력으로 유지한다. |
| import 혼선 | 실행 위치에 따라 import가 달라지는 문제 | `vds.` 기준 import로 통일한다. |
| 테스트 부재 | GUI에서만 동작 확인하는 문제 | Core/Presenter 테스트를 우선 유지한다. |

---

## 15. 문서 체계

VDS 문서는 다음 역할로 분리한다.

| 문서 | 역할 |
|---|---|
| `00_project_plan.md` | 왜 만들고, 누구를 위해, 어디까지 만들지 정의한다. |
| `00_boundary_map.md` | 요구사항/설계/구현의 경계를 구분한다. |
| `01_requirements.md` | 시스템이 외부에서 관찰 가능하게 해야 할 일을 정리한다. |
| `02_architecture.md` | 책임 분리와 의존 방향을 정리한다. |
| `03_implementation_notes.md` | 실제 파일, 클래스, 리팩토링 계획을 정리한다. |
| `04_mvp_checklist.md` | 현재 구현해야 할 작업 체크리스트를 관리한다. |

---

## 16. MVP 체크리스트

### 16.1 Core

- [ ] Stack.push(value)가 정상 동작한다.
- [ ] Stack.pop()이 최상단 값을 제거하고 반환한다.
- [ ] Stack.top()이 최상단 값을 반환하되 제거하지 않는다.
- [ ] Stack.clear()가 전체 값을 제거한다.
- [ ] 빈 Stack에서 pop/top 시 EmptyStackError가 발생한다.
- [ ] snapshot()이 내부 리스트의 안전 복사본을 반환한다.

### 16.2 Scene

- [ ] Scene 모델 위치를 확정한다.
- [ ] RectItem, TextItem, ArrowItem 구조를 확정한다.
- [ ] SceneMeta에 title, complexity, notes를 포함한다.
- [ ] Drawable key 규칙을 정한다.

### 16.3 Presenter

- [ ] Stack 상태를 Scene으로 변환한다.
- [ ] 빈 Stack 상태도 Scene으로 표현한다.
- [ ] TOP 포인터를 표시한다.
- [ ] 각 Stack 요소의 값이 TextItem으로 표시된다.

### 16.4 View

- [ ] Tkinter Canvas가 Scene을 렌더링한다.
- [ ] View는 Stack 객체를 직접 참조하지 않는다.
- [ ] RectItem/TextItem/ArrowItem을 각각 그릴 수 있다.
- [ ] render(scene) 호출 시 화면이 갱신된다.

### 16.5 App

- [ ] 프로그램 실행 시 메인 윈도우가 열린다.
- [ ] 입력창이 있다.
- [ ] push 버튼이 있다.
- [ ] pop 버튼이 있다.
- [ ] top 버튼이 있다.
- [ ] clear 버튼이 있다.
- [ ] 오류 메시지 표시 영역이 있다.

### 16.6 테스트

- [ ] Core 테스트가 통과한다.
- [ ] Presenter 테스트가 통과한다.
- [ ] Scene item 개수를 검증한다.
- [ ] 주요 Drawable key를 검증한다.

---

## 17. 향후 확장 방향

MVP가 안정화된 이후 다음 방향으로 확장한다.

| 확장 방향 | 설명 |
|---|---|
| Queue Visualizer | enqueue/dequeue/front 상태 시각화 |
| List Visualizer | insert/delete/search 과정 시각화 |
| Heap Visualizer | 삽입/삭제 후 heapify 과정 시각화 |
| Step Replay | 이전/다음 단계 이동 및 연산 기록 재생 |
| Animation | Scene 간 전환을 부드럽게 표현 |
| 학습 설명 강화 | 각 연산의 시간복잡도, 개념 설명, 주의점 표시 |

---

## 18. 최종 정리

VDS의 현재 개발 기준은 다음과 같이 정리한다.

```text
1. VDS는 자료구조 학습용 시각화 도구이다.
2. 1차 MVP는 Stack Visualizer로 제한한다.
3. 핵심 흐름은 Core → Presenter → Scene → View이다.
4. View는 자료구조를 직접 알지 않고 Scene만 렌더링한다.
5. 애니메이션, Replay, 다른 자료구조는 Stack MVP 이후로 미룬다.
6. 현재 목표는 확장 가능한 완벽한 엔진보다, Stack 하나가 제대로 보이는 학습 도구를 완성하는 것이다.
```

가장 중요한 기준은 다음 문장이다.

> 지금은 “확장 가능한 완벽한 엔진”을 만드는 단계가 아니라, “Stack 하나가 제대로 보이는 학습 도구”를 완성하는 단계이다.
