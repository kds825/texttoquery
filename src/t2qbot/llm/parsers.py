import re

def extract_sql(text: str) -> str:
    # ✅ t는 무조건 여기서 정의됨 (어떤 입력이 와도 안전)
    t = (text or "").strip()
    if not t:
        return ""

    # 1) ```sql ... ``` 코드블록이면 그 안만
    m = re.search(r"```(?:sql)?\s*(.*?)```", t, flags=re.IGNORECASE | re.DOTALL)
    if m:
        t = m.group(1).strip()

    # 2) SELECT부터 시작하는 부분만 남김
    m2 = re.search(r"(?is)\bselect\b.*", t)
    if m2:
        t = m2.group(0).strip()

    # 3) 세미콜론이 있으면 첫 문장까지만 (설명 붙는 거 제거)
    if ";" in t:
        t = t.split(";", 1)[0].strip()

    return t
