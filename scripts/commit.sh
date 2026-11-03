#!/usr/bin/env bash
# 커밋 한 명령(늘 같은 명령이라 승인 창에서 p 한 번이면 다시 안 묻는다)
#   탭 1: .commit-msg(메시지 한 줄) · .commit-files(파일 경로 한 줄에 하나) 를 쓰고  bash .agents/kit/commit.sh
#   탭 N: .commit-msg-N · .commit-files-N 을 쓰고  bash .agents/kit/commit.sh N
t=${1:+-$1}; m=".commit-msg$t"; f=".commit-files$t"
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" || exit 1
[ -s "$m" ] || { echo "메시지 파일 $m 이 비었습니다. 한 줄 쓰고 다시"; exit 1; }
[ -s "$f" ] || { echo "파일 목록 $f 이 비었습니다. 커밋할 파일 경로를 한 줄에 하나씩 쓰고 다시"; exit 1; }
lock="$(git rev-parse --git-dir)/index.lock"
for i in 1 2 3 4 5 6 7 8; do [ -e "$lock" ] || break; sleep 1; done
files=(); while IFS= read -r x || [ -n "$x" ]; do x="${x%$'\r'}"; [ -n "${x// }" ] && files+=("$x"); done < "$f"
git add -A -- "${files[@]}" || exit 1
if git diff --cached --quiet -- "${files[@]}"; then echo "커밋할 변경 없음"; : > "$m"; : > "$f"; exit 0; fi
git commit -q -F "$m" -- "${files[@]}" || exit 1
git log -1 --format='커밋 %h · %s'
: > "$m"; : > "$f"
