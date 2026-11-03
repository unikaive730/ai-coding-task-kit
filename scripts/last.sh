#!/usr/bin/env bash
# 지난 커밋 한눈에 보기 (사람이 Codex 를 기다리는 동안, 토큰 0): bash .agents/kit/last.sh [커밋 수, 기본 1]
n=${1:-1}
git rev-parse -q --verify HEAD >/dev/null || { echo "커밋 없음"; exit 0; }
base=$(git rev-parse -q --verify "HEAD~$n" 2>/dev/null || git hash-object -t tree /dev/null)
git log -n "$n" --date=format:%H:%M --format='== %h %ad · %s' --stat=100 | grep -v '^$'
rows() { git diff "$base" HEAD -- "$1" 2>/dev/null | grep '^+|' | grep -v -e '^+|---' -e '^+| *시각' -e '^+| *대상' | sed 's/^+//' | tail -"$2"; }
d=$(rows docs/DECISIONS.md 8); [ -n "$d" ] && { echo "== 새 결정 줄"; echo "$d"; }
v=$(rows docs/VERIFICATION.md 5); [ -n "$v" ] && { echo "== 새 검증 줄"; echo "$v"; }
s=$(git status --short | grep -v '^??' | head -5); [ -n "$s" ] && { echo "== 아직 커밋 안 된 변경"; echo "$s"; }
exit 0
