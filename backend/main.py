
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
import models

from routers import auth,farm,field,crop,activity,season,input,expenses,harvest,history,query


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title="AgriAi API",
    version="0.1.0",
    lifespan=lifespan
)


# Register routers
app.include_router(auth.router)
app.include_router(farm.router)
app.include_router(field.router)
app.include_router(season.router)
app.include_router(crop.router)
app.include_router(activity.router)
app.include_router(input.router)
app.include_router(expenses.router)
app.include_router(harvest.router)
app.include_router(history.router)
app.include_router(query.router)



@app.get("/")
async def root():
    return {
        "message": "AgriAi API is running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
