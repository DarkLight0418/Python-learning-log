### Mini Project - Visual Data Structure

# 프로젝트 개요

## 구현 요구사항

Visual Data Structure(VDS)는 자료구조의 상태 변화와 연산 결과를 **장면(Scene) 프레임** 단위로 시각화하는 학습용 도구로서, 이 시스템은 GUI 사용자와 테스트 시뮬레이터를 지원하며, 각 연산의 결과를 일관된 Scene 형식으로 생성해야 함.

## 소개

Python으로 간단히 자료구조들을 애니메이션으로 보여주는 프로그램

## 목적

Python 활용 능력 향상을 위해 작성


## 폴더 구조

```
.
├── src/vds/
│   ├── animation  # 애니메이션
│   ├── app        # 애플리케이션 실행/조립
│   ├── core       # 자료구조, 도메인 규칙
│   ├── presenter  # Scene/View Model 생성, 상태 머신
│   ├── usecases   # 실행/단계 생성
│   ├── utils      # 골고루 쓰이는 유틸들
│   └── view       # 실제 렌더링 모듈(Pygame/Tkinter/Web 등)
└── tests

```

## 규칙

### 데이터 흐름 (만들 때마다 참고..)

**'MVP 구조'를 인식하고 작업할 것**

```
사용자 ↔ View ↔ Presenter ↔ Model
```
```
User Input(View) → Presenter → UseCase → StepSequence → Presenter(compile) → Scene → (Animation) → View(render)
```

## 요구사항 명세

(별도 md 작성중)
docs/requirement.md 참고


## 시스템 구상

### 순서

```
사용자 연산 입력
→ 자료구조 상태 변화
→ 변화 과정을 단계(step)로 분해
→ 각 단계를 scene으로 변환
→ 다음 버튼으로 step을 전진
→ 필요하면 그 step 안에서 짧은 애니메이션 재생
```

### 구조

```
Usecase → StepSequence
Presenter → StepSequence를 SceneSequence로 변환
View → Scene 하나를 렌더
Controller → 다음/이전 step 이동
```


* * *
업데이트 2026.03.11.