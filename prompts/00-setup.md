# 00 준비 · 과제 시작 직후 · 사람이 터미널 탭 1에서 (토큰 0)

```
git clone -q --depth 1 https://github.com/unikaive730/ai-coding-task-kit /tmp/kit && bash /tmp/kit/scripts/install.sh
codex
```

- 신뢰 확인에서 '신뢰' → `/status`(AGENTS 파일 · AGENTS.override.md 를 만들었는데 없으면 첫 요청 맨 앞에 `$kit-rules`) · `/skills`(4개) · 추론 medium(low 나 default 로 뜨면 `/model` 에서 같은 모델 · Medium)
- 첫 줄(git clone)은 손으로 친다. 그 뒤 복사·붙여넣기: 터미널 붙여넣기는 Ctrl+Shift+V(맥 Cmd+V, Ctrl+V 아님), 복사는 선택 뒤 Ctrl+C · 선택 없이 누른 Ctrl+C 는 실행 중인 codex·서버를 멈춘다
- 첫 커밋 때 승인 창이 `git add` · `git commit` 차례로 두 번 뜬다 → 둘 다 '다시 묻지 않기'(p) · 판에 따라 커밋마다 `git commit` 창이 다시 뜨면 그때마다 p · 첫 명령부터 `bwrap: No permissions` 면 승인 창마다 p, 계속되면 '문제 신고' · git 이 없거나 접속이 막히면 README '설치가 아예 안 될 때' · 웹 과제는 첫 서버 검사 때 `python3 verify.py` 승인 창이 한 번 더 뜬다 → p · 그 밖의 즉석 검사 명령은 y
- 한도가 낮아지면 'Approaching rate limits · Switch to …?' 창이 뜬다 → 2 'Keep current model'. 기본 선택 1 은 모델을 바꾸니 카드를 붙이기 전에 화면 아래를 보고 Enter 만 누르지 않는다
