# ai-coding-task-kit

제한 시간 안에 코딩 에이전트(Codex 등)와 함께 과제를 푸는 작업 공간용 범용 지침 모음.
특정 과제의 풀이는 들어 있지 않다. 설치 없이 도는 것(bash · 표준 라이브러리)만 쓴다.

General-purpose working rules, skills, prompt cards and stdlib-only templates for time-boxed tasks done with a coding agent. No task-specific solutions.

## 넣는 법 (사람이 터미널에서, 토큰 0)

```bash
git clone -q --depth 1 https://github.com/unikaive730/ai-coding-task-kit /tmp/kit && bash /tmp/kit/scripts/install.sh
codex        # 신뢰 확인에서 '신뢰' → /status 로 AGENTS.md · /skills 로 스킬 확인
```

- 설치가 git 도 맡는다: 저장소가 아니면 `git init` 뒤 과제 파일을 '과제 제공 파일'로, 새로 넣은 파일만 '공개 작업 도구 설치'로 커밋한다 (끄기 `KIT_NO_GIT=1`). git 이름이 없으면 넣는 명령을 안내한다
- `git` 명령이 없을 때만: `mkdir -p /tmp/kit && curl -sL https://codeload.github.com/unikaive730/ai-coding-task-kit/tar.gz/main | tar xz -C /tmp/kit --strip-components=1 && bash /tmp/kit/scripts/install.sh`
- 접속이 차단돼 안 되면 다른 경로를 찾지 않는다. 플랫폼의 '문제 신고'를 하고 아래 '설치가 아예 안 될 때'로 진행한다
- 설치는 사람이 한다. Codex 기본 권한(workspace-write)에서는 `.agents` · `.git` 이 읽기 전용이라 승인 창이 뜬다
- 이미 있는 파일은 덮어쓰지 않는다. 과제에 AGENTS.md 가 있으면 그대로 두고 `AGENTS.override.md` 에 과제 지침 + 작업 원칙을 합친다 (합쳐서 30KB 가 넘으면 스킬 `kit-rules` 만 넣고 첫 요청에 `$kit-rules` 를 붙이라고 안내). `/status` 의 AGENTS 목록에 AGENTS.override.md 가 없는 판이면 첫 요청 맨 앞에 `$kit-rules` 를 붙인다
- 신뢰하지 않은 폴더에서는 AGENTS.md 를 읽지 않는 판이 있다. 신뢰 확인에서 '신뢰'를 고른다
- `/skills` 또는 `$` 로 스킬 4개(handoff · interview-requirements · plan-delegate · verify-submit)를 확인한다. 안 보이면 `mkdir -p .codex && mv .agents/skills .codex/skills` 후 codex 를 새로 시작한다. 두 곳에 같이 두면 같은 스킬이 두 번 뜬다
- 설치가 끝나면 `docs/ENV.md`(파이썬·노드·패키지·바깥 접속) 와 `docs/DATA_PROFILE.md`(CSV·XLSX 점검과 '확인할 것') 가 생긴다

### 설치가 아예 안 될 때 (첫 요청에 직접 친다)
```
작업 원칙: 코드보다 docs/AGREEMENT.md(과제 요구·성공 기준 숫자·범위·데이터 해석)를 먼저 채운다.
모르는 것은 지어내지 말고 실무자에게 물을 질문(한 질문 한 주제, 데이터 사실 포함)으로 돌려준다.
30분 이하 단위로 나눠 docs/STATUS.md 에 적고, 단위마다 실행·검증해 docs/VERIFICATION.md 에 명령·기대·실제를 남긴다.
결정·이유·버린 대안은 docs/DECISIONS.md. 표준 라이브러리 우선, 서버는 0.0.0.0, 답은 짧게.
```

## 쓰는 법

카드 파일 `.agents/kit/CARDS.md` 를 에디터에 열어 두고, 코드 블록 안만 복사해 `<...>` 를 채워 codex 에 붙인다. 탐색기에 `.agents` 가 안 보이면 Ctrl+P 로 `CARDS.md` 를 찾거나 터미널에서 `cat .agents/kit/CARDS.md` 로 보고 복사한다. 카드는 모두 요청 4요소(목표 · 맥락 · 제약 · 완료 조건)로 되어 있다.

| 언제 | 카드 | 스킬 |
|---|---|---|
| 과제 시작 직후 | `00-setup` (터미널 명령) | |
| 설치 직후 | `01-start` 과제 요구 표 · 첫 질문 3개 | `$interview-requirements` |
| 실무자 답을 받을 때마다 | `02-interview` | `$interview-requirements` |
| 성공 기준이 숫자로 정해진 뒤 | `03-plan` 30분 단위 계획 | `$plan-delegate` |
| 단위마다 | `04-build` | |
| 파일이 겹치지 않는 단위가 있을 때 | `05-parallel` (터미널 탭 2의 새 codex) | |
| 결과 숫자를 믿기 전에 | `06-verify` | `$verify-submit` |
| 제출 30분 전 | `07-docs` | |
| 제출 15분 전 | `08-submit` 점검표 · 후속 질문 대비 5줄 | `$verify-submit` |
| 압축이 한 번 일어났거나 큰 단위가 바뀔 때 | `09-handoff` → `/new` | `$handoff` |
| 같은 오류가 두 번 날 때 | `10-stuck` | |

- 스킬은 `$이름` 으로 부른다. 본문이 바로 들어가 파일을 따로 읽지 않으므로 토큰이 덜 든다
- 스킬을 못 읽는 판이어도 AGENTS.md 에 흐름·질문 순서·요청 4요소·검증·넘김 기준이 다 들어 있다
- 서버는 사람이 다른 터미널 탭에서 띄우고 그 탭을 닫지 않는다. 커밋도 사람이 단위마다 한다

## 들어 있는 것

| 경로 | 설치 위치 | 내용 |
|---|---|---|
| `AGENTS.md` | `AGENTS.md` (또는 `AGENTS.override.md`) | 작업 원칙: 흐름 · 합의 문서 · 실무자 질문 · 요청과 나눔 · 구현 · 검증 · 기록 · 토큰 · 하지 않는 것 |
| `.agents/skills/interview-requirements` | 같음 | 과제 파악 · 질문 순서 · 데이터 함정 목록 · 답 정리 |
| `.agents/skills/plan-delegate` | 같음 | 30분 단위 나눔 · STATUS 형식 · 요청 틀 · 나란히 맡기기 |
| `.agents/skills/verify-submit` | 같음 | 단위 검증 · 제출 점검표 · 후속 질문 대비 요약 |
| `.agents/skills/handoff` | 같음 | 넘길 때 · HANDOFF 내용 · 새 채팅 첫 요청 |
| `prompts/00~10` | `.agents/kit/CARDS.md` (한 파일로 합침) | 단계별 프롬프트 카드 |
| `docs-templates/` | `docs/` | AGREEMENT · STATUS · DECISIONS · VERIFICATION · HANDOFF 틀 |
| `scripts/install.sh` | | 설치 (덮어쓰기 없음) · git 첫 커밋 · 환경 점검 · 데이터 점검 |
| `scripts/envcheck.sh` | `docs/ENV.md` 를 만든다 | python · node · git · codex 판 · 파이썬 패키지 · pypi/npm/github 접속 · 메모리 |
| `templates/data/profile_data.py` | `.agents/kit/templates/data` | CSV·TSV·XLSX 점검: 중복 · 빈 칸 · 표기만 다른 값 · 시간대·날짜 형식·단위 섞임 · `--by 열` 묶음별 범위 |
| `templates/report/report.py` | `.agents/kit/templates/report` | 한 장 HTML 보고서: 숫자 타일 · 표 · 막대 · 선(기준선·사건 표시) SVG, 다크 모드 |
| `templates/web-python` | `.agents/kit/templates/web-python` | 표준 라이브러리 서버 (0.0.0.0:8000) · JSON API · 정적 화면 |
| `templates/web-node` | `.agents/kit/templates/web-node` | Node 내장 모듈 서버 (0.0.0.0:3000) · JSON API · 정적 화면 |
| `domain/semiconductor.md` | `.agents/kit/domain` | 반도체 제조 데이터 용어 · 과제 유형 · 점검표 요약 |

## 로컬에서 연습할 때
- 윈도우에서 codex 셸이 `CryptUnprotectData failed` 로 실패하면 `-c 'windows.sandbox="unelevated"'` 를 붙인다
- Codex 는 AGENTS.md 를 32KiB 까지만 읽고 뒤는 경고 없이 버린다. 설치 스크립트가 넘으면 알려 준다

## License
MIT
