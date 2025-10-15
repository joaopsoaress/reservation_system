from pydantic import BaseModel
from datetime import date, time

class SlotBase(BaseModel):
    date: date
    hour: str  # Using string "HH:MM:SS"
    duration: int

class SlotCreate(SlotBase):
    pass

class SlotOut(SlotBase):
    id: int
    status: str

    class Config:
        from_attributes = True