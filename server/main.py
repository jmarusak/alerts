import pytz
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from store import Store
from yahoo import get_alert_matches
from pushover import send_alert
from api import router as api_router

def inject_store():
    return store

store = Store()
store.import_alerts()

@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=repeat_task, trigger='interval', minutes=10)
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
    new_york_tz = pytz.timezone('America/New_York')
    timestamp = datetime.now(new_york_tz)
    print(f'Heartbeat at {timestamp.isoformat()}')

    # Get the current time in New York
    current_time = timestamp.time()

    # Define the stock market hours (9:15 AM to 4:15 PM)
    market_open = datetime.strptime('09:15', '%H:%M').time()
    market_close = datetime.strptime('16:15', '%H:%M').time()

    # Check if the current time is within market hours
    if market_open <= current_time <= market_close:
        messages = get_alert_matches(store)
        for message in messages:
            send_alert(message)
            print(f'Alert: {message}')
