# 이든 브랜드 소개 페이지 (DPP 진입 화면)

서스테이너블랩의 브랜드 이든(Idden) 팝업스토어용 모바일 페이지 시안. 크리에이티브코드 DPP(디지털 제품 여권) 실증 사업에 쓰임.

- 동작 흐름: 제품에 붙은 QR 스캔 → 이 브랜드 소개 페이지 → 하단 "이 제품 정보 확인하기" 버튼 → 스캔한 제품의 DPP 화면
- 시안 미리보기: `index.html`을 정적 서버로 열면 됨(아래 실행 방법 참고)

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `index.html` | 배포용 결과물. 글꼴(Pretendard 부분 글꼴)이 안에 들어간 단일 HTML |
| `build/src.html` | 원본 소스. 수정은 여기서 함 |
| `build/build.py` | `src.html`에 쓰인 글자만 골라 Pretendard를 부분 글꼴로 만들고 `index.html`을 생성 |
| `build/font/PretendardVariable.woff2` | Pretendard 원본(OFL) |
| `img/` | 페이지 이미지(이든 공식몰, biosite 제품 사진, 영상 포스터) |
| `film/idden-film.mp4` | 페이지 상단 영상(51초, 4:5, 음악 포함, 웹용 3.7MB) |
| `film/idden-film-music.mp4` | SNS용 고화질 음악 버전 |
| `film/idden-film-master.mp4` | 무음 고화질 원본 |
| `idden-film/` | 영상 원본 프로젝트(HyperFrames, HTML로 만든 영상). `SPEC.md`, `REVIEW.md`에 구성과 편집 이력 |
| `build/make_film_v4.py` | 영상 장면 12개를 생성하는 스크립트 |
| `test/e2e.mjs` | Playwright 점검(73항목: 가로 넘침, 스와이프, 대비, DPP 버튼 등) |
| `DESIGN.md`, `PRODUCT.md` | 디자인 기준(색, 글꼴, 움직임)과 제품 맥락 |
| `design-ref/` | 디자인 레퍼런스(awesome-design-md의 Oura, Airbnb DESIGN.md) |

## 실행 방법

```bash
# 페이지 미리보기
python -m http.server 8765
# 브라우저에서 http://localhost:8765 (모바일 화면 크기로 확인)

# src.html 수정 후 index.html 다시 만들기 (fonttools, brotli 필요)
pip install fonttools brotli
python build/build.py

# 점검 (Chrome 설치 필요)
cd test && npm install && node e2e.mjs
```

## 개발 요청 사항

### 1. DPP 연결 (필수)
- QR 주소에 제품 식별자를 붙여 이 페이지로 보냄. 예: `https://<도메인>/?pid=HB03-EARTHBAR`
- `build/src.html` 하단 스크립트의 `DPP_BASE`에 DPP 화면 주소를 넣으면, 버튼이 `DPP_BASE + pid`로 연결됨
- 현재는 `DPP_BASE`가 비어 있어서 버튼을 누르면 "시안 화면입니다" 안내만 뜸
- pid가 없거나 잘못된 경우의 처리(브랜드 공통 정보 화면 등) 정의 필요

### 2. 배포
- 정적 파일이라 어떤 호스팅에도 올릴 수 있음(GitHub Pages, S3+CloudFront 등)
- 영상은 3.7MB. 팝업스토어 현장 통신 환경을 고려해 CDN 사용 권장
- 영상은 자동재생 무음으로 시작하고 "소리 켜기" 버튼을 눌러야 음악이 나옴(모바일 자동재생 정책)

### 3. 화면 구성
1. 상단 51초 브랜드 필름 + 소리 켜기, 일시정지 버튼
2. 한 줄 소개
3. "버려지던 부산물이 제품이 되기까지" 가로 스와이프 7장(이전/다음 버튼, 점 표시, 키보드 지원)
4. "이렇게 만든 이든의 제품" 4종
5. 언론 보도 가로 스크롤, 더 알아보기 링크(idden.co, 인스타그램)
6. 하단 고정 DPP 버튼

### 4. 디자인 기준 (DESIGN.md 요약)
- 색: 흰 바탕 `#FFFFFF`, 짙은 초록 `#193B2A` 하나만 주색. 다크 모드 토큰 별도 정의
- 글꼴: Pretendard 한 종류(제목 300/600, 본문 400). 영상의 영문 제목은 Outfit
- 움직임: 버튼 누름 0.97배 160ms, 스와이프 버튼 이동 약 0.5초 감속 곡선, 호버는 마우스 환경에서만
- "움직임 줄이기" 설정 시 영상 자동재생과 전환 애니메이션을 끔

### 5. 출시 전 확인 필요
- 문구 확인(서스테이너블랩): "제품이 팔릴수록 보르네오의 숲이 자랍니다", 얼스바의 맥주 효모 원료 언급, 스타터 키트 포장 구성
- 영상 음악: 사용자 제공 무료 비트(여름 타입비트 "Summuer"). 제작자의 이용 조건과 크레딧 표기 확인 필요
- 영상 통계 출처: OECD Global Plastics Outlook(2022, 2019년 기준), 자원재활용법 개정(2024.3.29 시행, 객실 50실 이상 숙박업소)
- 대표, 보르네오 사진은 원본 해상도가 낮음(900~950px). 고해상도 원본 수급 시 교체
- 이미지 출처: 이든 공식몰(idden.co), 이든 프랑스 파트너 biosite

## 영상 수정 방법
```bash
cd idden-film
npx hyperframes@0.9.15 preview      # 브라우저 편집기
npx hyperframes@0.9.15 check        # 검사
npx hyperframes@0.9.15 render --quality high --output ../film/idden-film-music.mp4
```
장면 문구와 시간은 `build/make_film_v4.py`에서 고친 뒤 `python build/make_film_v4.py`로 다시 생성함. 단, 이 스크립트는 `index.html`을 덮어쓰므로 음악 태그(`#bgm`)를 다시 넣어야 함(`idden-film/REVIEW.md` 참고).
