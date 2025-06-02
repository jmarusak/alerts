from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router
from alert import Alert
from store import Store

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

store.add_or_update(Alert(symbol='AAPL', below=180.0, above=220.0, last='2025-05-29T10:00'))
store.add_or_update(Alert(symbol='NVDA', below=135.0, above=143.0, last='2025-05-29T11:24'))
store.add_or_update(Alert(symbol='GOOG', below=2500.0, above=2700.0, last='2025-05-28T16:45'))

app.include_router(api_router)
