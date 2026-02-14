from fastapi import FastAPI
from t2qbot.config.settings import get_settings
from t2qbot.api.routes_health import router as health_router
from t2qbot.api.routes_chat import router as chat_router

app = FastAPI(title="Text2Query Bot")

app.include_router(health_router)
app.include_router(chat_router, prefix = "/v1")
