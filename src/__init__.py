# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router
from src.reviews.routes import review_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Starting Up...")
    await init_db()
    yield
    print("Application shutting down...")


version = "v1"

app = FastAPI(
    title="Bookly API",
    description="A Rest API for a book review web service",
    version=version,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Authentication"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])
