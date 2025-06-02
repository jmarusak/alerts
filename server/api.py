from fastapi import APIRouter, HTTPException, Depends
from alert import Alert
from store import Store

router = APIRouter()


@router.post('/alert')
def add_or_update_alert(alert: Alert, store: Store = Depends()):
    result = store.add_or_update(alert)
    return {'status': result, 'current_alerts': store.get_all()}

@router.delete('/alert/{symbol}')
def delete_alert(symbol: str, store: Store = Depends()):
    success = store.delete(symbol)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found.")
    return {'status': 'deleted', 'current_alerts': store.get_all()}

@router.get('/alerts')
def get_all_alerts(store: Store = Depends()):
    return store.get_all()
