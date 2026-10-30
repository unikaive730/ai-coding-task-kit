#!/usr/bin/env bash
# 작업 공간에 작업 원칙·스킬·문서 틀·프롬프트 카드·틀을 넣는다. 이미 있는 파일은 덮어쓰지 않는다.
# 사용: bash <kit>/scripts/install.sh [작업 폴더]
# 사람이 터미널에서 돌린다 (Codex 의 기본 권한으로는 .agents · .git 에 쓸 수 없다). 설치 뒤 codex 를 새로 시작한다.
# git: 저장소가 아니면 git init 뒤 과제 파일을 첫 커밋으로, 설치한 파일을 두 번째 커밋으로 남긴다. git 이름이 없으면 이 저장소에만 넣는다. 끄기: KIT_NO_GIT=1
set -e
KIT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:-$PWD}"
cd "$DEST"

GIT=""; FIRSTFAIL=""
if [ -z "$KIT_NO_GIT" ] && command -v git >/dev/null 2>&1; then
  NEWREPO=""; git rev-parse --git-dir >/dev/null 2>&1 || { git init -q && echo "git init 했습니다."; NEWREPO=1; }
  # git 이름이 없으면 이 저장소에만 넣는다 (없으면 설치 커밋과 Codex 커밋이 모두 실패한다)
  ID=""; git config user.name >/dev/null 2>&1 || { git config user.name "응시자"; ID=1; }
  git config user.email >/dev/null 2>&1 || { git config user.email "candidate@localhost"; ID=1; }
  [ -n "$ID" ] && echo "git 이름이 없어 이 저장소에만 '응시자'로 넣었습니다."
  if [ -n "$NEWREPO" ]; then
    # 50MB 넘는 제공 파일은 커밋에서 뺀다 (설치가 느려지고 디스크를 두 배로 쓰지 않게)
    big=$(find . -path ./.git -prune -o -type f -size +50M -print 2>/dev/null | sed 's|^\./|/|')
    if [ -n "$big" ]; then
      printf '%s\n' "$big" >> .git/info/exclude
      echo "50MB 넘는 파일 $(printf '%s\n' "$big" | wc -l | tr -d ' ')개는 커밋에서 뺐습니다 (.git/info/exclude)."
    fi
    git add -A
    git diff --cached --quiet || git commit -qm "과제 제공 파일" || { FIRSTFAIL=1; echo "첫 커밋 실패. 아래 안내대로 커밋합니다."; }
  fi
  GIT=1
fi
mkdir -p .agents/skills .agents/kit docs

NEW=() # 이번에 새로 만든 것 (이것만 커밋한다)
put() { # put <원본> <대상> : 대상이 없을 때만 복사
  if [ -e "$2" ]; then echo "  그대로 둠: $2"; else mkdir -p "$(dirname "$2")"; cp -r "$1" "$2"; NEW+=("$2"); fi
}

# 1. 작업 원칙
if [ -e .agents/kit/AGENTS.from-kit ] || cmp -s AGENTS.md "$KIT/AGENTS.md" 2>/dev/null; then
  echo "  그대로 둠: AGENTS.md (이 도구가 넣은 것)"
elif [ -f AGENTS.md ]; then
  echo "과제에 AGENTS.md 가 있어 그대로 둡니다."
  if [ ! -e .agents/skills/kit-rules ]; then
    mkdir -p .agents/skills/kit-rules
    { printf -- '---\nname: kit-rules\ndescription: 시간 제한 과제 작업 원칙(합의 문서 · 실무자 질문 · 계획 · 검증 · 기록 · 토큰). 작업을 시작할 때, 새 채팅을 열 때, 막힐 때 읽는다.\n---\n\n'
      cat "$KIT/AGENTS.md"; } > .agents/skills/kit-rules/SKILL.md
    NEW+=(.agents/skills/kit-rules)
  fi
  total=$(( $(wc -c < AGENTS.md) + $(wc -c < "$KIT/AGENTS.md") ))
  if [ ! -e AGENTS.override.md ] && [ "$total" -lt 30000 ]; then
    { cat AGENTS.md
      printf '\n\n---\n\n<!-- 아래는 공개 작업 도구 ai-coding-task-kit 의 작업 원칙. 위 과제 지침이 우선한다 -->\n\n'
      cat "$KIT/AGENTS.md"; } > AGENTS.override.md
    NEW+=(AGENTS.override.md)
    echo "AGENTS.override.md 에 과제 AGENTS.md + 작업 원칙을 합쳤습니다 (Codex 는 이 파일을 대신 읽습니다)."
    echo "  과제 AGENTS.md 가 바뀌면: rm AGENTS.override.md 후 이 스크립트를 다시 돌립니다."
  elif [ ! -e AGENTS.override.md ]; then
    echo "합치면 30KB 가 넘어 합치지 않았습니다. 첫 요청 맨 앞에 \$kit-rules 를 붙이세요."
  fi
else
  cp "$KIT/AGENTS.md" AGENTS.md && echo "kit" > .agents/kit/AGENTS.from-kit
  NEW+=(AGENTS.md .agents/kit/AGENTS.from-kit)
fi

# 2. 스킬 · 문서 틀 · .gitignore (과제에 없을 때만. 캐시 파일을 커밋에서 뺀다, 지우기가 막혀도 섞이지 않게)
if [ ! -e .gitignore ]; then printf '%s\n' '__pycache__/' '*.pyc' '.pytest_cache/' '.venv/' 'node_modules/' > .gitignore; NEW+=(.gitignore); fi
for d in "$KIT"/.agents/skills/*/; do put "$d" ".agents/skills/$(basename "$d")"; done
for f in "$KIT"/docs-templates/*.md; do put "$f" "docs/$(basename "$f")"; done

# 3. 프롬프트 카드(한 파일) · 틀 · 분야 요약
if [ ! -e .agents/kit/CARDS.md ]; then
  { echo "# 프롬프트 카드 (코드 블록 안만 복사해 <...> 를 채워 codex 에 붙인다)"; echo
    for f in "$KIT"/prompts/*.md; do cat "$f"; printf '\n---\n\n'; done; } > .agents/kit/CARDS.md
  NEW+=(.agents/kit/CARDS.md)
fi
for d in "$KIT"/templates/*/; do put "$d" ".agents/kit/templates/$(basename "$d")"; done
put "$KIT/domain" .agents/kit/domain
find .agents/kit -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true

# 4. 환경 점검 · 데이터 점검 (토큰 0)
if [ ! -e docs/ENV.md ]; then bash "$KIT/scripts/envcheck.sh" docs/ENV.md || true; [ -e docs/ENV.md ] && NEW+=(docs/ENV.md); fi
PY=""; for c in python3 python; do "$c" -c "import sys" >/dev/null 2>&1 && PY="$c" && break; done
if [ ! -e docs/DATA_PROFILE.md ] && [ -n "$PY" ]; then
  data=()
  while IFS= read -r f; do data+=("$f"); done < <(find . -path ./.agents -prune -o -path ./.git -prune -o -path ./node_modules -prune -o \
    -type f \( -iname '*.csv' -o -iname '*.tsv' -o -iname '*.xlsx' \) -size -200M -print 2>/dev/null | sort | head -20)
  if [ ${#data[@]} -gt 0 ]; then
    "$PY" "$KIT/templates/data/profile_data.py" "${data[@]}" > docs/DATA_PROFILE.md 2>&1 || true
    NEW+=(docs/DATA_PROFILE.md)
    echo "데이터 점검: docs/DATA_PROFILE.md (${#data[@]}개 파일, '확인할 것'이 실무자 질문 후보)"
  fi
fi

# 5. git: 캐시 파일 제외 · 설치한 파일만 커밋
if [ -n "$GIT" ]; then
  ex="$(git rev-parse --git-dir)/info/exclude"; mkdir -p "$(dirname "$ex")"
  grep -qx '__pycache__/' "$ex" 2>/dev/null || printf '%s\n' '__pycache__/' '*.pyc' '.pytest_cache/' '.venv/' 'node_modules/' >> "$ex"
  if [ ${#NEW[@]} -gt 0 ] && git add -- "${NEW[@]}" 2>/dev/null && ! git diff --cached --quiet -- "${NEW[@]}"; then
    if git commit -qm "공개 작업 도구 설치 (ai-coding-task-kit)" -- "${NEW[@]}"; then echo "커밋: 공개 작업 도구 설치 (새로 넣은 ${#NEW[@]}개만)"
    else msg="공개 작업 도구 설치"; [ -n "$FIRSTFAIL" ] && msg="과제 제공 파일 + 공개 작업 도구 설치"
      echo "커밋 실패: git config user.name \"<이름>\" && git config user.email \"<메일>\" 뒤 git commit -qm \"$msg\""; fi
  fi
fi

# 6. 크기 경고 (Codex 는 32KiB 뒤를 경고 없이 버린다)
f=AGENTS.md; [ -e AGENTS.override.md ] && f=AGENTS.override.md
[ "$(wc -c < "$f")" -gt 32768 ] && echo "경고: $f 가 $(wc -c < "$f")바이트입니다. 32KiB 뒤는 Codex 가 읽지 않습니다."

echo
echo "설치 끝: $f · .agents/skills ($(ls .agents/skills | tr '\n' ' ')) · docs/*.md · .agents/kit"
echo "다음: codex → 신뢰 확인에서 '신뢰' → /status · /skills 확인 → 카드 01 붙이기"
echo "  커밋은 Codex 가 요청마다 스스로 한다. 첫 커밋 때 승인 창이 git add · git commit 차례로 두 번 뜬다 → 둘 다 '다시 묻지 않기'(p)."
[ -e AGENTS.override.md ] && echo "  /status 의 AGENTS 목록에 AGENTS.override.md 가 없으면 첫 요청 맨 앞에 \$kit-rules 를 붙입니다."
echo "카드: .agents/kit/CARDS.md (에디터로 열어 두고 복사 → 터미널에는 Ctrl+Shift+V, 탐색기에 안 보이면 Ctrl+P 로 CARDS.md) · 스킬은 \$이름 으로 부른다 (\$interview-requirements · \$plan-delegate · \$verify-submit · \$handoff)"
