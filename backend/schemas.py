from pydantic import BaseModel
import datetime

class SlotBase(BaseModel):
    date: datetime.date
    hour: datetime.time
    duration: int

    model_config = {
        "from_attributes": True  # substitui orm_mode=True
    }

class SlotOut(BaseModel):
    id: int
    date: datetime.date
    hour: datetime.time
    duration: int
    status: str

class SlotCreate(SlotBase):
    pass

class SlotRead(SlotBase):
    id: int

    class Config:
        orm_mode = True