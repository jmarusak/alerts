from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from alert import Alert
from store import Store

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# CORS so React frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust this for production
    allow_methods=["*"],
    allow_headers=["*"],
)

store = Store()

store.add_or_update(Alert(symbol="AAPL", below=180.0, above=220.0, last="2025-05-29T10:00"))
store.add_or_update(Alert(symbol="NVDA", below=135.0, above=143.0, last="2025-05-29T11:24"))
store.add_or_update(Alert(symbol="GOOG", below=2500.0, above=2700.0, last="2025-05-28T16:45"))

@app.post("/alert")
def add_or_update_alert(alert: Alert):
    result = store.add_or_update(alert)
    return {"status": result, "current_alerts": store.get_all()}

@app.delete("/alert/{symbol}")
def delete_alert(symbol: str):
    success = store.delete(symbol)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "deleted", "current_alerts": store.get_all()}

@app.get("/alerts")
def get_all_alerts():
    return store.get_all()
