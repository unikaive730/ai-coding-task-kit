#!/usr/bin/env bash
# 작업 공간에 지침·스킬·문서 틀을 넣는다. 이미 있는 파일은 덮어쓰지 않는다.
# 사용: git clone <이 저장소> /tmp/kit && bash /tmp/kit/scripts/install.sh [작업 폴더]
# 설치 뒤 codex 를 새로 시작해야 AGENTS.md 를 읽는다.
set -e
KIT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:-$PWD}"
cd "$DEST"

mkdir -p .agents/skills docs

if [ -f AGENTS.md ]; then
  echo "AGENTS.md 가 이미 있어 그대로 둡니다. 이 지침은 스킬 kit-rules 로 넣습니다."
  mkdir -p .agents/skills/kit-rules
  {
    printf -- '---\nname: kit-rules\ndescription: 시간 제한 과제 작업 원칙(합의 문서 · 계획 · 검증 · 기록 · 토큰). 작업을 시작할 때와 막힐 때 읽는다.\n---\n\n'
    cat "$KIT/AGENTS.md"
  } > .agents/skills/kit-rules/SKILL.md
else
  cp "$KIT/AGENTS.md" AGENTS.md
fi

for d in "$KIT"/.agents/skills/*/; do
  name="$(basename "$d")"
  [ -e ".agents/skills/$name" ] || cp -r "$d" ".agents/skills/$name"
done

for f in "$KIT"/docs-templates/*.md; do
  b="$(basename "$f")"
  [ -e "docs/$b" ] || cp "$f" "docs/$b"
done

echo "설치 끝: AGENTS.md · .agents/skills ($(ls .agents/skills | tr '\n' ' ')) · docs/*.md"
echo "웹·데이터 틀: $KIT/templates · 반도체 요약: $KIT/domain/semiconductor.md (필요할 때만 복사)"
