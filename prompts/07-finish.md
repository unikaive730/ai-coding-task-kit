# 07 문서·제출 점검 · 제출 30분 전, 한 요청으로

```
$verify-submit 목표: 문서·제출 점검을 한 번에 해. README(실행 한 줄·구조·결과 숫자·한계)·DECISIONS·STATUS 를 실제 출력과 git log 에 맞춰.
맥락: 제출 마감 <시각>. 제약: 새 기능 금지, 5분 안에 못 고칠 것은 목록으로만. 깨끗한 clone(mktemp)에서 README 명령을 그대로 돌려(서버는 검사 스크립트 안에서 PORT=0).
완료: 커밋 뒤 git status --short 가 비면 끝. 답은 점검 결과 5줄 이내 + 후속 질문 대비 요약 5줄.
```

- 요청이 8번을 넘었으면 `/new` → '어디서 실행'(Where should the new conversation run?) 창에서 1(Use current Git worktree) → 빈 입력 칸이 보인 뒤 붙인다(2 는 다른 폴더 복사본이라 커밋이 거기 쌓인다. HANDOFF 없이 docs·git log 로 충분) · 5줄 요약은 사람이 직접 읽는다. 후속 서술형은 AI 없이 직접 쓴다
