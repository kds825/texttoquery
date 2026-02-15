import json
import requests
import pandas as pd
import streamlit as st
from datetime import datetime

DEFAULT_API_URL = "http://127.0.0.1:8000/v1/chat"

st.set_page_config(page_title="Text-To-SQL Chatbot", page_icon="🧠", layout="centered")

#----Minimal CSS Polish ----
st.markdown(
    """
    <style>
    .block-container { padding-top: 1.8rem; padding-bottom: 2rem; max-width: 980px;}
    [data-testid="stChatMessage"] { padding: 0.75rem 0.9rem; border-radius: 14px; }
    .sqlbox code { font-size: 0.9rem !important; }
    .small-muted { color: rgba(255,255,255,0.65); font-size: 0.85rem; }
    .badge { display:inline-block; padding: 0.2rem 0.55rem; border-radius: 999px;
            background: rgba(255,255,255,0.08); font-size: 0.8rem; }
    .kpi { padding: 0.65rem 0.8rem; border-radius: 14px; background: rgba(255,255,255,0.06); }
    .stDataFrame { border-radius: 14px; overflow: hidden; }
    </style>    
    """,
    unsafe_allow_html=True,
)

def _as_table(rows):
    """rows(list[dict] or list[list]) ->pandas DataFrame"""
    if rows is None:
        return None
    if isinstance(rows, list) and len(rows) ==0:
        return pd.DataFrame()
    if isinstance(rows, list) and isinstance(rows[0], dict):
        return pd.DataFrame(rows)
    #fallback : show raw
    return None

def call_api(api_url: str, message: str, timeout: int=60):
    r=requests.post(api_url, json={"message": message}, timeout=timeout)
    try:
        data = r.json()
    except Exception:
        data ={"detail": r.text}
    return r.status_code, data

#----- Sidebar -----
with st.sidebar:
    st.title("🧪 실험 설정")
    api_url = st.text_input("API URL", value=DEFAULT_API_URL, help="FastAPI 서버의 /v1/chat 주소")
    timeout = st.slider("요청 타임아웃(초)", min_value=10, max_value=180, value=60, step=5)
    
    st.divider()
    st.caption("빠른 질문")
    quick = st.radio(
        "선택해서 바로 테스트",
        [
            "customers 테이블 전체 보여줘",
            "서울 고객만 보여줘",
            "평균 spend보다 spend가 큰 고객은?",
            "도시별 평균 spend를 구해줘",
            "가장 최근 가입한 고객은?",
        ],
        index=2,
    )
    if st.button("📨 선택 질문 보내기", use_container_width = True):
        st.session_state["_send_quick"] = quick
    
    st.divider()
    if st.button("🧹 대화 초기화", use_container_width=True):
        st.session_state.message=[]
        st.session_state.stats ={"calls":0, "last_ms":None}
        
# ---- Header ----
st.markdown("## 🧠 Text-to-SQL Chatbot")
st.markdown(
    "<span class = 'badge'>FastAPI</span> <span class='badge'>LLM</span> <span class='badge'>SQLite</span>",
    unsafe_allow_html=True,
)
st.markdown("<div class='small-muted'>자연어로 질문하면 SQL을 만들고, DB 결과를 표로 보여줍니다.</div>",unsafe_allow_html=True)
st.write("")

# ---- Session state ----
if "messages" not in st.session_state:
    st.session_state.messages = []
if "stats" not in st.session_state:
    st.session_state.stats={"calls": 0, "last_ms": None}
    
# ---- KPI row ----
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='kpi'>📞 호출 수<br><b>{}</b></div>".format(st.session_state.stats["calls"]), unsafe_allow_html=True)
with c2:
    ms = st.session_state.stats["last_ms"]
    st.markdown("<div class='kpi'>⏱️ 마지막 응답<br><b>{}</b></div>".format(f"{ms} ms" if ms is not None else "-"), unsafe_allow_html=True)
with c3:
    st.markdown("<div class='kpi'>🔗 엔드포인트<br><b>/v1/chat</b></div>", unsafe_allow_html=True)

st.write("")

# ---- Render chat history ----
for msg in st.session_state.messages:
    role = msg["role"]
    with st.chat_message(role):
        st.write(msg["content"])
        if role == "assistant" and msg.get("sql"):
            with st.expander("🧾 생성된 SQL 보기", expanded=False):
                st.code(msg["sql"],language="sql")
        if role == "assistant" and msg.get("rows") is not None:
            df = _as_table(msg["rows"])
            if df is not None: 
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.code(json.dumps(msg["rows"], ensure_ascii=False, indent =2), language="json")
                
    
# ---- Input ----
user_text = st.chat_input("예 : 서울 고객 평균 spend? / 평균보다 spend 큰 고객은?")

# quick send
if st.session_state.get("_send_quick"):
    user_text = st.session_state.pop("_send_quick")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    with st.chat_message("assistant"):
        with st.spinner("생각 중...(SQL 만들고 실행하는 중)"):
            start = datetime.now()
            try:
                status, data = call_api(api_url, user_text, timeout=timeout)
                ms = int((datetime.now()-start).total_seconds()*1000)
                st.session_state.stats["calls"] +=1
                st.session_state.stats["last_ms"]=ms
                
                if status ==200:
                    sql =data.get("sql", "")
                    rows=data.get("rows",[])
                    st.success("성공 ✅")
                    st.write("결과를 가져왔어요.")
                    with st.expander("🧾 생성된 SQL 보기", expanded=False):
                        st.code(sql, language="sql")
                    df = _as_table(rows)
                    if df is not None:
                        st.dataframe(df, use_container_width = True, hide_index=True)
                    else:
                        st.code(json.dumps(rows, ensure_ascii=False, indent=2), language="json")
                        
                    st.session_state.messages.append(
                        {"role": "assistant", "content" : "요청을 처리했어요.", "sql":sql, "rows":rows}
                    )
                else:
                    detail = data.get("detail", data)
                    st.error("서버 에러 ❌")
                    st.code(str(detail))
                    st.session_state.messages.append(
                        {"role": "assistant", "content": f"에러: {detail}"}
                    )
            except requests.exceptions.RequestException as e:
                st.error("서버 연결 실패 ❌")
                st.code(str(e))
                st.session_state.messages.append(
                    {"role":"assistant", "content":f"서버 연결 실패: {e}"}
                )