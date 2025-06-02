import asyncio
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router
from alert import Alert
from store import Store
from loop import start_background_loop

app = FastAPI()

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

@app.on_event("startup")
async def startup_event():
    await start_background_loop(store)
