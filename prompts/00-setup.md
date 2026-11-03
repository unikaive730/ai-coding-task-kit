# 00 준비 · 과제 시작 직후 · 사람이 터미널 탭 1에서 (토큰 0)

```
git clone -q --depth 1 https://github.com/unikaive730/ai-coding-task-kit /tmp/kit && bash /tmp/kit/scripts/install.sh
codex
```

- 터미널 탭은 넷으로 나눠 이름을 바꿔 둔다(탭 이름 더블클릭): 1 구현(codex) · 2 검사(codex, 카드 05) · 3 사람 셸(`last.sh`·결과 보기) · 4 서버(웹 과제만, 닫지 않는다). 에디터에는 CARDS.md 만 열어 둔다(채워서 저장해도 git 에 안 잡힌다)
- 신뢰 확인에서 '신뢰' → `/status`(AGENTS 파일 · AGENTS.override.md 를 만들었는데 없으면 첫 요청 맨 앞에 `$kit-rules`) · `/skills`(4개) · 추론은 기본이 low 일 수 있다: `/model` → GPT-6.1-Sol → Medium 을 직접 고르고 아래 줄로 확인(`/effort` 는 없다). 탭 2·5 도 같은 단계
- 첫 줄(git clone)은 손으로 친다. 사용자 이름·비밀번호를 물으면 입력하지 말고 저장소 주소 철자(unikaive730/ai-coding-task-kit)부터 다시 본다. 그 뒤 복사·붙여넣기: 터미널 붙여넣기는 Ctrl+Shift+V(맥 Cmd+V, Ctrl+V 아님), 복사는 선택 뒤 Ctrl+C · 선택 없이 누른 Ctrl+C 는 실행 중인 codex·서버를 멈춘다
- 첫 커밋 때 승인 창 `bash .agents/kit/commit.sh` 가 뜬다 → '다시 묻지 않기'(p) 한 번이면 끝까지 안 뜬다 · Codex 가 `git add`·`git commit` 을 따로 부르는 창이면 둘 다 p · 첫 명령부터 `bwrap: No permissions` 면 승인 창마다 p, 계속되면 '문제 신고' · git 이 없거나 접속이 막히면 README '설치가 아예 안 될 때' · 웹 과제는 첫 서버 검사 때 `python3 verify.py` 승인 창이 한 번 더 뜬다 → p · 그 밖의 즉석 검사 명령은 y. 단 LLM·외부 주소(LLM_BASE_URL·http)를 부르는 명령이면 esc(3 No) 를 누르고 "가짜 응답으로 시험해" 한 줄 · LLM 과제의 verify.py 는 실제 LLM 을 안 부르는 것을 본 뒤 p
- 한도가 낮아지면 'Approaching rate limits · Switch to …?' 창이 뜬다 → 2 'Keep current model'. 기본 선택 1 은 모델을 바꾸니 카드를 붙이기 전에 화면 아래를 보고 Enter 만 누르지 않는다 · 이 창은 요청이 끝난 직후에 뜨니 카드마다 붙이기 전에 아래 줄 모델 이름이 GPT-6.1-Sol medium 인지 본다 · 붙인 카드가 사라지고 아래 줄이 GPT-6-Luna 로 바뀌었으면 창에 먹힌 것 → `/model` → GPT-6.1-Sol → Medium → s(이 세션만) → 카드를 다시 붙인다
- 시계는 화면 위 남은 시간(180분 기준): 0:55 쯤 06 · 늦어도 0:30 에 07 · 0:25 에 브리핑 · 0:15 에 읽던 중이어도 제출 시작. 실무자 창에 메시지를 보낸 뒤마다 탭 1·2·5 아래 줄을 본다: 승인 창은 위 p·y·esc · `? 1 question · shift+← to answer` 면 shift+← 로 열어 한 줄 답 · `Selected model is at capacity` 로 끊겼으면 모델을 바꾸지 말고 같은 탭에 `방금 끊겼어. 하던 요청을 이어서 끝내` 한 줄 · 답에 일본어가 섞이면 `한국어로만 다시`
- 에디터에 글을 치기 전에 커서가 터미널에 있는지 본다(md 파일은 누르면 편집 상태로 열리고 자동 저장된다) · 파일 조작은 터미널로(GUI 탐색기는 느리다) · `/skills` 에 4개가 안 보이면 플랫폼 도움말에 '이 환경의 Skill 적용 방법'을 한 번 묻는다
