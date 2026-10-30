# 00 준비 · 과제 시작 직후 · 사람이 터미널 탭 1에서 (토큰 0)

```
git clone -q --depth 1 https://github.com/unikaive730/ai-coding-task-kit /tmp/kit && bash /tmp/kit/scripts/install.sh
codex
```

- 설치가 git 을 맡는다: 저장소가 아니면 git init 과 '과제 제공 파일' 커밋, 이어서 새로 넣은 파일만 '공개 작업 도구 설치' 커밋
- `git` 명령이 없을 때만: `mkdir -p /tmp/kit && curl -sL https://codeload.github.com/unikaive730/ai-coding-task-kit/tar.gz/main | tar xz -C /tmp/kit --strip-components=1 && bash /tmp/kit/scripts/install.sh`
- 접속이 차단돼 안 되면 다른 경로를 찾지 않는다. '문제 신고' 뒤 첫 요청에 작업 원칙 4줄을 직접 친다(README '설치가 아예 안 될 때')
- codex 첫 화면의 신뢰 확인에서 '신뢰'를 고른다. 고르지 않으면 AGENTS.md 를 읽지 않는 판이 있다
- `/status` 로 모델·권한·AGENTS 파일 확인 (AGENTS.override.md 를 만들었는데 목록에 없으면 첫 요청 맨 앞에 `$kit-rules`) · `/model` 은 권장 모델, 추론은 medium (문서 정리는 low)
- `/skills` 로 스킬 4개 확인 (과제에 AGENTS.md 가 있었으면 kit-rules 까지 5개). 안 보이면 `mkdir -p .codex && mv .agents/skills .codex/skills` 뒤 codex 다시 시작
- 서버는 탭 2에서 사람이 띄우고 그 탭은 닫지 않는다. 커밋도 사람이: `git add -A && git commit -qm "무엇을·왜"`
