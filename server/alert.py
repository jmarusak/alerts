from pydantic import BaseModel

class Alert(BaseModel):
    symbol: str
    below: float
    above: float
    last: str  # ISO timestamp as string
