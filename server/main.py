from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from alert import Alert
from store import Store
from yahoo import get_alert_matches
from pushover import send_alert
from api import router as api_router

def inject_store():
    return store

store = Store()
store.add_or_update(Alert(symbol='NVDA', below=112, above=135, last=''))

@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=repeat_task, trigger='interval', seconds=10)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory='static', html=True), name='static')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router)
app.dependency_overrides[Store] = inject_store

async def repeat_task():
    messages = get_alert_matches(store)
    for message in messages:
        send_alert(message)
