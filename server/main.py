from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router

app = FastAPI()

app.mount('/static', StaticFiles(directory='static', html=True), name='static')

# CORS so React frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router)
