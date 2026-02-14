import asyncio
from sqlalchemy import text
from t2qbot.db.engine import engine

SQL = """
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    spend INTEGER,
    joined_at TEXT
);

INSERT INTO customers (name, city, spend, joined_at) VALUES
('Alice', 'Seoul', 120, '2025-01-10'),
('Bob', 'Seoul', 80, '2025-03-03'),
('Chris', 'Busan', 200, '2025-02-14'),
('Dina', 'Incheon', 50, '2025-04-22');
"""

async def main():
    async with engine.begin() as conn:
        for stmt in SQL.split(";"):
            if stmt.strip():
                await conn.execute(text(stmt))
                
    print("Database seeded: local.db created")

if __name__ =="__main__":
    asyncio.run(main())