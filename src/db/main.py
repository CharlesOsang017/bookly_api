# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
# pyrefly: ignore [missing-import]
from sqlmodel import SQLModel
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker
# pyrefly: ignore [missing-import]
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config
from src.books.models import Book

# Make sure Config.DATABASE_URL uses an async driver like postgresql+asyncpg://
engine: AsyncEngine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Create an async session factory bound to the engine instance
async_session_maker = sessionmaker(
    bind=engine,                  # Pass the engine instance, not the class
    class_=AsyncSession,          # Use class_= with a trailing underscore
    expire_on_commit=False
)

async def get_session() -> AsyncSession:      # Type-hint returning AsyncSession generator
    async with async_session_maker() as session:
        yield session