from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from t2qbot.config.settings import get_settings

settings = get_settings()
engine = create_async_engine(settings.db_url, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit= False)
