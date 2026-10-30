#!/usr/bin/env bash
# 작업 환경 점검. 사람이 터미널에서 한 번 돌린다(토큰 0). install.sh 가 자동으로 부른다.
# 사용: bash envcheck.sh [결과 파일]   기본: docs/ENV.md · 바깥 접속 확인은 주소마다 최대 3초
out="${1:-docs/ENV.md}"
mkdir -p "$(dirname "$out")"
PY=""
for c in python3 python; do "$c" -c "import sys" >/dev/null 2>&1 && PY="$c" && break; done
ver() { command -v "$1" >/dev/null 2>&1 && "$@" 2>&1 | head -1 || echo "없음"; }
net() { command -v curl >/dev/null 2>&1 || { echo "curl 없음"; return; }
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "$1" 2>/dev/null); [ "${code:-000}" = "000" ] && echo "안 됨" || echo "됨($code)"; }
{
  echo "# 작업 환경 ($(date '+%Y-%m-%d %H:%M'))"
  echo
  echo "| 항목 | 값 |"
  echo "|---|---|"
  echo "| python | $( [ -n "$PY" ] && "$PY" --version 2>&1 || echo 없음) ($PY) |"
  echo "| pip | $( [ -n "$PY" ] && "$PY" -m pip --version 2>/dev/null | cut -d' ' -f1-2 || echo 없음) |"
  echo "| node · npm | $(ver node --version) · $(ver npm --version) |"
  echo "| git | $(ver git --version) |"
  echo "| codex | $(ver codex --version) |"
  if [ -n "$PY" ]; then
    mods=$(PYTHONIOENCODING=utf-8 "$PY" - <<'PYEOF' 2>/dev/null
import importlib
have, miss = [], []
for m in ["pandas", "numpy", "openpyxl", "matplotlib", "sklearn", "scipy", "statsmodels", "plotly", "fastapi", "uvicorn", "flask", "pytest", "requests"]:
    try:
        have.append(f"{m} {getattr(importlib.import_module(m), '__version__', '')}".strip())
    except Exception:
        miss.append(m)
print("있음: " + (", ".join(have) or "-") + " / 없음: " + (", ".join(miss) or "-"))
PYEOF
)
    echo "| 파이썬 패키지 | $mods |"
  fi
  echo "| pypi 접속 | $(net https://pypi.org/simple/pip/) |"
  echo "| npm 접속 | $(net https://registry.npmjs.org/) |"
  echo "| github 접속 | $(net https://github.com) |"
  if [ -r /proc/meminfo ]; then
    echo "| 메모리 | $(awk '/MemTotal|MemAvailable/{printf "%s %d MB  ", $1, $2/1024}' /proc/meminfo) |"
  fi
  echo "| CPU | $(nproc 2>/dev/null || echo ?)개 |"
  echo "| 디스크(이 폴더) | $(df -h . 2>/dev/null | awk 'NR==2{print $4" 남음 / "$2}') |"
  echo
  echo "- 패키지가 '없음'이고 pypi 접속이 '안 됨'이면 표준 라이브러리로 만든다"
} > "$out"
echo "환경 점검: $out"
sed -n '5,20p' "$out" | cut -c1-160
