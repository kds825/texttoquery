import re

def extract_sql(text: str) -> str:
    '''
    LLM이 생성한 텍스트에서 실행 가능한 SELECT SQL 문만 추출하는 함수.

    동작 과정:
    1. ```sql ... ``` 형태의 마크다운 코드 블록이 있으면 그 안의 내용만 추출한다.
    2. SELECT 키워드부터 시작하는 부분만 남긴다.
    3. 세미콜론(;) 이후에 붙는 설명 문장은 제거한다.
    4. 최종적으로 하나의 안전한 SQL 문장만 반환한다.

    LLM이 설명을 같이 붙여서 반환하는 경우를 대비한
    사전 정제(클린업)용 필터 함수이다.
    '''
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
