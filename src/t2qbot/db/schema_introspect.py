from sqlalchemy import text
from t2qbot.db.engine import SessionLocal

async def get_schema() -> str:
    async with SessionLocal() as session:
        result = await session.execute(
            text("""
                 SELECT name
                 FROM sqlite_master
                 WHERE type='table'
                    AND name NOT LIKE 'sqlite_%'
                 ORDER BY name;
        """)
        )
        
        tables = [r[0] for r in result.fetchall()]
        schema_text = ""
        
        for table in tables:
            schema_text += f"\nTable: {table}\n"
            
            cols = await session.execute(text(f"PRAGMA table_info({table});"))
            for col in cols.fetchall():
                #col format: cid, name, type, notnull, dflt_value, pk
                schema_text += f"- {col[1]} ({col[2]})\n"
        return schema_text.strip()