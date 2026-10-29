"""표 데이터 첫 점검 (CSV·XLSX).

실행: python profile_data.py <파일> [<파일> ...]
출력: 크기 · 열 형식 · 빈 칸 · 중복 행 · 숫자 요약 · 자주 나오는 값 · 단위·날짜 의심 열
pandas 가 필요하다 (pip install pandas openpyxl).
"""
import re
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning)


def load(path):
    if path.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    for enc in ("utf-8", "utf-8-sig", "cp949"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, encoding="latin-1")


def profile(path):
    df = load(path)
    print(f"\n=== {path}")
    print(f"행 {len(df)} · 열 {df.shape[1]} · 완전 중복 행 {int(df.duplicated().sum())}")
    nulls = df.isna().sum()
    print("\n[열 형식 · 빈 칸]")
    for col in df.columns:
        print(f"  {col!s:30} {str(df[col].dtype):10} 빈 칸 {int(nulls[col])}")
    num = df.select_dtypes("number")
    if not num.empty:
        print("\n[숫자 요약]")
        print(num.describe().T.to_string())
    print("\n[자주 나오는 값 · 의심]")
    unit_re = re.compile(r"[0-9.,]+\s*([A-Za-z%가-힣]+)")
    for col in df.columns:
        s = df[col].dropna()
        if s.empty:
            continue
        if s.dtype == object or pd.api.types.is_string_dtype(s):
            top = s.astype(str).value_counts().head(5)
            print(f"  {col}: " + " | ".join(f"{k}({v})" for k, v in top.items()))
            units = s.astype(str).str.extract(unit_re)[0].dropna().unique()
            if len(units) > 1:
                print(f"    ! 단위가 섞였을 수 있음: {list(units)[:6]}")
            parsed = pd.to_datetime(s.astype(str), errors="coerce")
            if 0.5 < parsed.notna().mean() < 1:
                print(f"    ! 날짜로 안 읽히는 값 {int(parsed.isna().sum())}개")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for p in sys.argv[1:]:
        profile(p)
