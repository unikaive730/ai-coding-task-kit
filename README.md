# ai-coding-task-kit

제한 시간 안에 코딩 에이전트(Codex 등)와 함께 과제를 푸는 작업 공간용 범용 지침 모음.
특정 과제의 풀이는 들어 있지 않다.

General-purpose working rules, skills and templates for time-boxed tasks done with a coding agent. No task-specific solutions.

## 넣는 법

```bash
git clone https://github.com/unikaive730/ai-coding-task-kit /tmp/kit
bash /tmp/kit/scripts/install.sh      # 지금 폴더에 AGENTS.md · .agents/skills · docs/ 틀
codex                                  # 설치 뒤 새로 시작해야 AGENTS.md 를 읽는다
```

- 이미 있는 파일은 덮어쓰지 않는다. 과제에 AGENTS.md 가 있으면 이 지침은 스킬 `kit-rules` 로 들어간다

## 들어 있는 것

| 경로 | 내용 |
|---|---|
| `AGENTS.md` | 작업 원칙: 합의 문서 → 계획·나눔 → 구현 → 검증 → 기록 · 토큰 아끼기 · 하지 않는 것 |
| `.agents/skills/interview-requirements` | 업무 담당자에게 물을 질문 순서와 정리 방법 |
| `.agents/skills/plan-delegate` | 30분 단위 나눔 · 요청 틀(목표·맥락·제약·완료 조건) |
| `.agents/skills/verify-submit` | 검증 기록 · 제출 전 점검표 |
| `.agents/skills/handoff` | 대화가 길어질 때 새 채팅으로 넘기는 문서 |
| `docs-templates/` | AGREEMENT · STATUS · DECISIONS · VERIFICATION · HANDOFF 틀 |
| `templates/web-python` | FastAPI 최소 서버 (0.0.0.0:8000) |
| `templates/web-node` | Node 내장 모듈만 쓰는 최소 서버 (0.0.0.0:3000) |
| `templates/data/profile_data.py` | CSV·XLSX 첫 점검(빈 칸·중복·단위·날짜) |
| `domain/semiconductor.md` | 반도체 제조 데이터 용어·과제 유형·점검표 요약 |

## 첫 요청 예시

```
AGENTS.md 를 읽고 README 와 제공 파일을 살펴서 docs/AGREEMENT.md 의 '과제 요구' 표를 채워.
모르는 칸은 '추정'으로 두고, 업무 담당자에게 물을 질문 3개를 제안해. 코드는 아직 쓰지 마.
```

## License
MIT
