# ai-coding-task-kit

제한 시간 안에 코딩 에이전트(Codex 등)와 함께 과제를 푸는 작업 공간용 범용 지침 모음.
특정 과제의 풀이는 들어 있지 않다. 설치 없이 도는 것(bash · 표준 라이브러리)만 쓴다.

General-purpose working rules, skills, prompt cards and stdlib-only templates for time-boxed tasks done with a coding agent. No task-specific solutions.

## 넣는 법 (사람이 터미널에서, 토큰 0)

```bash
git clone -q --depth 1 https://github.com/unikaive730/ai-coding-task-kit /tmp/kit && bash /tmp/kit/scripts/install.sh
codex        # 신뢰 확인에서 '신뢰' → /status 로 AGENTS.md · /skills 로 스킬 확인
```

- 설치가 git 도 맡는다: 저장소가 아니면 `git init` 뒤 과제 파일을 '과제 제공 파일'로, 새로 넣은 파일만 '공개 작업 도구 설치'로 커밋한다 (끄기 `KIT_NO_GIT=1`). git 이름이 없으면 이 저장소에만 '응시자'로 넣는다. `.gitignore` 가 없으면 캐시 파일(`__pycache__/` 등)을 빼는 것을 만든다
- `git` 명령이 없을 때만: `mkdir -p /tmp/kit && curl -sL https://codeload.github.com/unikaive730/ai-coding-task-kit/tar.gz/main | tar xz -C /tmp/kit --strip-components=1 && bash /tmp/kit/scripts/install.sh`
- 접속이 차단돼 안 되면 다른 경로를 찾지 않는다. 플랫폼의 '문제 신고'를 하고 아래 '설치가 아예 안 될 때'로 진행한다
- 설치는 사람이 한다. Codex 기본 권한(workspace-write)에서는 `.agents` · `.git` 이 읽기 전용이라 승인 창이 뜬다. 그 뒤 Codex 의 첫 커밋 때 승인 창이 `git add` · `git commit` 차례로 두 번 뜬다. 둘 다 '다시 묻지 않기'(p)를 고르면 새 탭의 codex 도 다시 묻지 않는다(판에 따라 커밋 메시지까지 묶여 저장돼 커밋마다 다시 뜨면 그때마다 p)
- 이미 있는 파일은 덮어쓰지 않는다. 과제에 AGENTS.md 가 있으면 그대로 두고 `AGENTS.override.md` 에 과제 지침 + 작업 원칙을 합친다 (합쳐서 30KB 가 넘으면 스킬 `kit-rules` 만 넣고 첫 요청에 `$kit-rules` 를 붙이라고 안내). `/status` 의 AGENTS 목록에 AGENTS.override.md 가 없는 판이면 첫 요청 맨 앞에 `$kit-rules` 를 붙인다
- 신뢰하지 않은 폴더에서는 AGENTS.md 를 읽지 않는 판이 있다. 신뢰 확인에서 '신뢰'를 고른다
- `/skills` 또는 `$` 로 스킬 4개(handoff · interview-requirements · plan-delegate · verify-submit)를 확인한다. 안 보이면 `mkdir -p .codex && mv .agents/skills .codex/skills` 후 codex 를 새로 시작한다. 두 곳에 같이 두면 같은 스킬이 두 번 뜬다
- 설치가 끝나면 `docs/ENV.md`(파이썬·노드·패키지·바깥 접속) 와 `docs/DATA_PROFILE.md`(CSV·XLSX 점검과 '확인할 것') 가 생긴다

### 설치가 아예 안 될 때 (첫 요청에 직접 친다)
```
작업 원칙: 코드보다 docs/AGREEMENT.md(과제 요구·성공 기준 숫자·범위·데이터 해석)를 먼저 채운다. 칸은 한 줄, 80줄 이하.
모르는 것은 지어내지 말고 실무자에게 한 메시지로 보낼 질문 3~5개(번호, 한 질문 한 주제, 데이터 사실 포함)로 돌려준다.
단위 3~4개로 나눠 docs/STATUS.md 에 적고, 단위마다 실행·검증해 docs/VERIFICATION.md 에 명령·기대·실제를 남기고 커밋한다.
결정·이유·버린 대안은 docs/DECISIONS.md 표 한 줄씩. 표준 라이브러리 우선, 서버는 0.0.0.0, 답은 5줄 이내.
```

## 쓰는 법

카드 파일 `.agents/kit/CARDS.md` 를 에디터에 열어 두고, 코드 블록 안만 복사해 `<...>` 를 채워 codex 에 붙인다. 터미널 붙여넣기는 Ctrl+Shift+V(맥 Cmd+V)이고, 선택 없이 누른 Ctrl+C 는 실행 중인 codex·서버를 멈춘다. 탐색기에 `.agents` 가 안 보이면 Ctrl+P 로 `CARDS.md` 를 찾거나 터미널에서 `cat .agents/kit/CARDS.md` 로 보고 복사한다. 카드는 모두 요청 4요소(목표 · 맥락 · 제약 · 완료 조건)로 되어 있다.

| 언제 | 카드 | 스킬 |
|---|---|---|
| 과제 시작 직후 | `00-setup` (터미널 명령) | |
| 설치 직후 | `01-start` 과제 요구 표 · 한 메시지로 보낼 질문 5개 | `$interview-requirements` |
| 실무자 답을 받을 때마다 | `02-interview` 반영 · 다음 질문 3개 이하 | `$interview-requirements` |
| 구현 중 실무자가 요구를 바꾸면 | `02-interview` 의 요구 변경 블록 → 질문 답은 02 → '다시' 단위부터 04 | `$interview-requirements` |
| 성공 기준이 숫자로 정해진 뒤 | `03-plan` 단위 3~4개 · 나란히 계약 | `$plan-delegate` |
| 단위마다 | `04-build` (성공 지표가 목표 미달이면 같은 카드의 조정 블록) | |
| 파일이 겹치지 않는 단위가 있을 때 | `05-parallel` (터미널 탭 3의 새 codex) | |
| 핵심 기능이 돈 뒤 | `06-verify` 연결 · 전체 테스트 · 숫자 대조 | `$verify-submit` |
| 제출 30분 전 | `07-finish` 문서·제출 점검 한 번에 · 후속 질문 대비 5줄 | `$verify-submit` |
| 같은 오류가 두 번 날 때 | `08-stuck` | |
| 압축이 한 번 일어났을 때 | `09-handoff` → `/new` | `$handoff` |

- 스킬은 `$이름` 으로 부른다. Codex 는 목록의 설명을 보고 SKILL.md 를 한 번 읽는다(대화마다 한 번)
- 스킬을 못 읽는 판이어도 AGENTS.md 에 흐름·질문 기준·문서 상한·요청 4요소·검증·커밋 기준이 다 들어 있다
- 커밋은 Codex 가 요청마다 실행 확인 뒤 스스로 한다(무엇을·왜 한 줄). 나란히 맡긴 대화는 자기 파일만 `git add` 해서 커밋한다
- 문서 상한: AGREEMENT 80줄 · STATUS 40줄 · VERIFICATION 40줄 · DECISIONS 는 표 한 줄씩. 요청마다 다시 읽는 문서라 길면 토큰이 늘어난다
- 서버는 사람이 다른 터미널 탭에서 띄우고 그 탭을 닫지 않는다. Codex 의 서버 검사는 `python3 verify.py` 한 명령 · PORT=0 이라 겹치지 않는다

## 들어 있는 것

| 경로 | 설치 위치 | 내용 |
|---|---|---|
| `AGENTS.md` | `AGENTS.md` (또는 `AGENTS.override.md`) | 작업 원칙: 흐름 · 합의 문서 · 실무자 질문 · 요청과 나눔 · 구현 · 검증 · 기록 · 토큰 · 하지 않는 것 |
| `.agents/skills/interview-requirements` | 같음 | 과제 파악 · 질문 순서 · 데이터 함정 목록 · 답 정리 |
| `.agents/skills/plan-delegate` | 같음 | 30분 단위 나눔 · STATUS 형식 · 요청 틀 · 나란히 맡기기 |
| `.agents/skills/verify-submit` | 같음 | 단위 검증 · 제출 점검표 · 후속 질문 대비 요약 |
| `.agents/skills/handoff` | 같음 | 넘길 때 · HANDOFF 내용 · 새 채팅 첫 요청 |
| `prompts/00~09` | `.agents/kit/CARDS.md` (한 파일로 합침) | 단계별 프롬프트 카드 (코드 블록 1~4줄) |
| `docs-templates/` | `docs/` | AGREEMENT · STATUS · DECISIONS · VERIFICATION · HANDOFF 틀 |
| `scripts/install.sh` | | 설치 (덮어쓰기 없음) · git 첫 커밋 · 환경 점검 · 데이터 점검 |
| `scripts/envcheck.sh` | `docs/ENV.md` 를 만든다 | python · node · git · codex 판 · 파이썬 패키지 · pypi/npm/github 접속 · 메모리 |
| `templates/data/profile_data.py` | `.agents/kit/templates/data` | CSV·TSV·XLSX 점검: 중복 · 빈 칸 · 표기만 다른 값(degC=C) · 줄임 표기(L1=line-1) · 시간대·날짜 형식(일/월/연)·단위 섞임 · 묶음별 범위(`--by 열`, 없으면 자동) |
| `templates/report/report.py` | `.agents/kit/templates/report` | 한 장 HTML 보고서: 숫자 타일 · 표 · 막대 · 선(기준선·사건 표시) SVG, 다크 모드 |
| `templates/web-python` | `.agents/kit/templates/web-python` | 표준 라이브러리 서버 (0.0.0.0:8000) · JSON API · 정적 화면 |
| `templates/web-node` | `.agents/kit/templates/web-node` | Node 내장 모듈 서버 (0.0.0.0:3000) · JSON API · 정적 화면 |
| `domain/semiconductor.md` | `.agents/kit/domain` | 반도체 제조 데이터 용어 · 과제 유형 · 점검표 요약 |

## 리눅스 작업 공간에서 알아 둘 것
- `python` 없이 `python3` 만 있을 수 있다. README 실행 명령은 실제로 돌린 쪽 그대로 쓴다 (`docs/ENV.md` 의 python 줄)
- 사람 셸에는 `rg` 가 없을 수 있다(`grep -rn`). Codex 안에서는 내장 rg 가 돈다
- 첫 명령부터 `bwrap: No permissions to create a new namespace` 면 샌드박스가 못 도는 환경이라 명령마다 승인 창이 뜬다. 승인 창마다 '다시 묻지 않기'(p), 계속되면 '문제 신고'
- 지우기(`rm`)가 막힐 수 있다. 캐시·임시 생성물은 지우지 말고 `.gitignore` 로 뺀다
- 깨끗한 상태 확인은 `d=$(mktemp -d)/c && git clone -q . "$d" && cd "$d"` 에서. 작업 폴더 안에 복사본·worktree 를 만들지 않는다
- 정적 HTML 미리보기: `python3 -m http.server 8000 --bind 0.0.0.0`
- Codex 샌드박스는 인터넷 소켓(서버 띄우기·curl)을 막아 서버 검사마다 승인 창이 뜬다. 검사를 `python3 verify.py <이름>` 한 명령에 모으면 첫 창에서 p 한 번으로 끝난다
- codex 0.166 의 `/new` 는 '어디서 실행' 창을 먼저 띄운다. 1(Use current Git worktree)을 고른 뒤 붙인다

## 로컬에서 연습할 때
- 윈도우에서 codex 셸이 `CryptUnprotectData failed` 로 실패하면 `-c 'windows.sandbox="unelevated"'` 를 붙인다
- Codex 는 AGENTS.md 를 32KiB 까지만 읽고 뒤는 경고 없이 버린다. 설치 스크립트가 넘으면 알려 준다

## License
MIT
