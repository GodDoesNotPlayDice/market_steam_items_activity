from pydantic import BaseModel
from typing import List, Optional

class Activity(BaseModel):
    action: str
    price: float
    timestamp: int

class MarketData(BaseModel):
    success: int
    activities: List[Activity]
