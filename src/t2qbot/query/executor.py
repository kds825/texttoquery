from sqlalchemy import text
from t2qbot.db.engine import SessionLocal
from t2qbot.config.settings import get_settings

settings = get_settings()

async def run(sql: str):
    if "limit" not in sql.lower():
        sql += f" LIMIT {settings.default_limit}"
        
    async with SessionLocal() as session:
        result = await session.execute(text(sql))
        rows = result.mappings().all()
        return [dict(r) for r in rows]
    