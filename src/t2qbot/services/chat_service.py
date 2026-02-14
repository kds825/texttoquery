from t2qbot.llm.client import LLMClient
from t2qbot.llm.parsers import extract_sql
from t2qbot.query.validator import validate
from t2qbot.query.executor import run
from t2qbot.db.schema_introspect import get_schema

async def handle(message: str):
    schema = await get_schema()
    
    prompt = f"""
You are a SQLite SQL generator.

Rules:
- Output ONLY a single SQL SELECT statement.
- Do NOT include any explanation.
- Do NOT include markdown fences.
- Do NOT include a trailing semicolon.

Schema:
{schema}

Question: {message}

SQL:
""".strip()
    llm = LLMClient()
    raw = await llm.generate(prompt)
    sql = extract_sql(raw)
    
    validate(sql)
    rows = await run(sql)
    
    return sql, rows