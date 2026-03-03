### Mini Project - Visual Data Structure

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
(별도 md 작성 예정)


* * *
업데이트 2026.03.02.