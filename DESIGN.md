# DESIGN — 이든 브랜드 소개 (Oura 레퍼런스 기반)

레퍼런스: design-ref/oura-DESIGN.md (awesome-design-md). 오우라의 규칙만 빌리고 로고, 이름, 고유 그래픽은 쓰지 않음.

## 색
2026-11-05 확정: 사용자 지시로 원래 시안(claude.ai/artifact/VLHKqSxJ7XAXcLnQXipNew) 색을 따름. 흰 바탕에 짙은 초록 한 가지를 주색으로 씀. 파랑, 크림은 쓰지 않음.
| 토큰 | 값 | 역할 |
|---|---|---|
| canvas, surface | #FFFFFF | 바탕, 카드 |
| sand | #EEF0E9 | 옅은 세이지 면(제품 카드, 원래 시안 히어로 #EDEEE6 계열) |
| ink | #172A20 | 제목, 본문 |
| stone | #4E5A53 | 보조 본문 |
| ash | #66716A | 메타 정보 |
| hairline | #E4E7E1 | 구분선 |
| forest | #193B2A | 주색. 강조 카드, 언론 띠, DPP 버튼 |

## 글꼴
Pretendard 하나만 씀. 오우라의 얇은 세리프 자리는 Pretendard 300 굵기로 대신함. 굵기가 아니라 크기로 위계를 만듦.
| 역할 | 크기 | 굵기 | 행간 |
|---|---|---|---|
| display | 46px | 300 | 1.08 |
| h2 | 30px | 300 | 1.25 |
| title | 20px | 600 | 1.35 |
| body | 16px | 400 | 1.65 |
| ui | 14px | 500 | 1.4 |
| meta | 13px | 400 | 1.45 |

## 형태
- 버튼은 완전 원형 알약형, 카드는 24px, 큰 제품 이미지는 32px 모서리.
- 그림자는 거의 없음. 면의 색 변화와 머리카락선으로 구분함.
- 제목 위 영문 라벨(eyebrow)은 쓰지 않음. 번호는 실제 순서(여정 6단계, 리추얼 3단계)에만 씀.

## 움직임 (Emil Kowalski 원칙)
- 누름: scale(0.97), 160ms, cubic-bezier(0.23,1,0.32,1)
- 호버는 (hover:hover) and (pointer:fine)에서만. 사진 1.03배 확대, 링크 카드 2px 상승
- 점 표시 폭 전환 200ms ease-out
- 스크롤 연동 등장 효과 없음. 5초 넘게 움직이는 필름에는 일시정지 버튼
- prefers-reduced-motion에서 모두 정지
