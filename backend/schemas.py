from pydantic import BaseModel
from datetime import date, time

    # Base schema for Slot
class SlotBase(BaseModel):
    date: date
    hour: str  # Using string "HH:MM:SS"
    duration: int

    # Schema for creating a Slot
class SlotCreate(SlotBase):
    pass

    # Schema for updating a Slot
class SlotOut(SlotBase):
    id: int
    status: str

    class Config:
        from_attributes = True