import asyncio
import datetime
from store import Store
from fastapi import Depends

async def update_alerts_timestamp(store: Store = Depends()):
    while True:
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        for alert in store.get_all():
            alert.last = now
        print(f"Updated alert timestamps at {now}")
        await asyncio.sleep(15 * 60)  # Wait 15 minutes

async def start_background_loop(store: Store = Depends()):
    asyncio.create_task(update_alerts_timestamp(store))
