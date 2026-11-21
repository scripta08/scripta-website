# 훈민정음학회 홈페이지 (scripta.kr)

정적 사이트(Eleventy) + 관리 화면(Decap CMS). 시안 A 디자인.

## 구조
- `src/_data/society.json` — **학회 정보 한 곳**: 임기, 회장, 회장 인사말, 임원진, 편집위원회, 연락처. 관리 화면의 "학회 정보"에서 고치면 머리말·바닥글·학회 조직·편집위원회·연락처·인사말 서명에 모두 반영됩니다.
- `src/notices/` 알림, `src/conferences/` 학술대회, `src/scripta/` 학술지 권호, `src/pages/ko|en/` 고정 페이지.
- `src/admin/` 관리 화면(/admin). `config.yml`의 `repo`, `base_url`을 학회 GitHub 조직 저장소와 로그인 연결 주소로 바꿔야 합니다.
- `src/files/` PDF·양식. 이관할 PDF 목록은 `scripts/pdf-manifest.csv`(백업 경로 → 사이트 경로).

## 명령
- `npm install` 후 `npm run build` → `_site/`에 결과물
- `npm run serve` → 로컬 미리보기
- 관리 화면 로컬 시험: `npx decap-server` 실행 후 `npm run serve`, 브라우저에서 /admin

## 이관 스크립트
- `scripts/import_backup.py` — 옛 XE 백업에서 뽑은 docs.json으로 콘텐츠 생성(한 번만 사용)
- `scripts/preview_relative.py` — 미리보기용 상대 경로 변환
