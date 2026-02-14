def validate(sql: str):
    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT allowed")
    
    forbidden = ["drop", "delete", "update", "insert", "alter"]
    for f in forbidden:
        if f in sql.lower():
            raise ValueError("Unsafe query detected")