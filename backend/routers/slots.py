from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import date, time

from backend.schemas import SlotCreate

router = APIRouter()

class SlotRead(BaseModel):
    id: int
    date: str
    hour: str
    duration: int
    status: str
    class Config:
        orm_mode = True

from backend.crud import get_slot, get_slots, create_slot, reserve_slot, update_slot, delete_slot

@router.get("/slots", response_model=List[SlotRead])
def read_slots():
    return get_slots()

@router.get("/slots/{slot_id}", response_model=SlotRead)
def read_slot(slot_id: int):
    return get_slot(slot_id)

@router.post("/slots", response_model=SlotRead)
def add_slot(slot: SlotRead):
    return create_slot(SlotCreate(**slot.dict()))

@router.put("/slots/{slot_id}/reserve", response_model=SlotRead)
def reserve(slot_id: int):
    return reserve_slot(slot_id)

@router.delete("/slots/{slot_id}")
def remove_slot(slot_id: int):
    return delete_slot(slot_id)