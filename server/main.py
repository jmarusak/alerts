from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router

from alert import Alert
from store import Store

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    # repeat task every 10 seconds
    scheduler.add_job(func=repeat_task, trigger='interval', seconds=10)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='static', html=True), name='static')

# CORS so React frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

store = Store()
store.add_or_update(Alert(symbol='', below=0, above=0, last=''))

app.include_router(api_router)

# Dependency to inject the store instance
def get_store():
    return store

app.dependency_overrides[Store] = get_store

async def repeat_task():
    print("Repeating task executed")
