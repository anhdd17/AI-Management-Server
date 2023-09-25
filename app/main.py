from fastapi import FastAPI
from config.db_config import Base, engine
from routers import user_router

# Create database tables
from models import user

user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router.router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

