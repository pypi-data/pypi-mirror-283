from typing import Optional

from pydantic import BaseModel


class Inquiry(BaseModel):
    price: float
    balance: float
    speed: int
    attempts: int


class CommonInfo(BaseModel):
    status: int
    count: int
    inquiry: Inquiry
    message: Optional[str] = None
