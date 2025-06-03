from datetime import datetime

import pytz
import yfinance as yf

from store import Store

def get_alert_matches(store: Store) -> list[str]:
    messages = []
    alerts = store.get_all()
    for alert in alerts:
        if alert.last == '':
            symbol = alert.symbol 
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="1d", interval="1d")
            if not history.empty:
                below = alert.below
                above = alert.above
                close = round(float(history['Close'].iloc[-1]), 2)

                if close <= below or close >= above:
                    new_york_tz = pytz.timezone('America/New_York')
                    timestamp = datetime.now(new_york_tz).isoformat()
                    alert.last = timestamp
                    message = f'{symbol}: {close}'
                    messages.append(message)

    return messages
