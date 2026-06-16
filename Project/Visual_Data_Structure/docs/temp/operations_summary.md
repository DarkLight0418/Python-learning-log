파일명:
operations.py

이 파일의 책임:
Usecase 실행 결과를 표준 형태로 표현한다.

이 파일이 의존하는 것:
dataclass, Enum, Any

이 파일을 의존하게 될 것:
StackPushUsecase, StackPopUsecase, QueueUsecase, Presenter, UI

핵심 클래스/함수:
OperationStatus, OperationResult, success(), failure(), ok

왜 이렇게 설계했는가:
Usecase마다 반환값이 달라지면 UI 처리 방식이 복잡해지므로 결과 형식을 통일하기 위해서이다.

좋은 점:
성공/실패 처리 방식이 명확하다.
snapshot이 tuple이라 안전하다.
frozen=True라 결과 객체가 불변이다.

불안한 점:
message가 Usecase에 들어가면 UI 문구와 Application 로직이 섞일 수 있다.
value와 snapshot이 Any라 타입 안정성이 낮다.

나중에 바뀔 수 있는 부분:
message 대신 message_code를 사용할 수 있다.
snapshot을 별도 Snapshot 모델로 분리할 수 있다.
Graph처럼 복잡한 자료구조는 별도 Result가 필요할 수 있다.

직접 해볼 변형 과제:
Stack push/pop usecase에서 OperationResult를 반환해보기.
빈 스택 pop 실패 케이스를 구현해보기.
Presenter가 result.ok 기준으로 출력 메시지를 다르게 처리하게 해보기.

오늘 이해한 한 문장:
OperationResult는 Usecase와 UI 사이에서 결과 전달 방식을 통일해주는 경계 객체이다.