from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date, time

from backend.schemas import SlotCreate, SlotOut
from backend.crud import get_slot, get_slots, create_slot, reserve_slot, update_slot, delete_slot

router = APIRouter()

@router.get("/slots", response_model=List[SlotOut])
async def read_slots():
    try:
        return await get_slots()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading slots: {str(e)}")

@router.get("/slots/{slot_id}", response_model=SlotOut)
async def read_slot(slot_id: int):
    try:
        slot = await get_slot(slot_id)
        if not slot:
            raise HTTPException(status_code=404, detail="Slot not found")
        return slot
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading slot: {str(e)}")

@router.post("/slots", response_model=SlotOut)
async def add_slot(slot: SlotCreate):
    try:
        # Additional validation for hour format
        if not isinstance(slot.hour, str) or len(slot.hour) > 8:
            raise HTTPException(status_code=400, detail="Hour must be a string in format 'HH:MM:SS'")
        
        return await create_slot(slot)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating slot: {str(e)}")

@router.put("/slots/{slot_id}/reserve", response_model=SlotOut)
async def reserve(slot_id: int):
    try:
        slot = await get_slot(slot_id)
        if not slot:
            raise HTTPException(status_code=404, detail="Slot not found")
        return await reserve_slot(slot_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reserving slot: {str(e)}")

@router.delete("/slots/{slot_id}")
async def remove_slot(slot_id: int):
    try:
        result = await delete_slot(slot_id)
        if not result["deleted"]:
            raise HTTPException(status_code=404, detail="Slot not found")
        return {"message": "Slot deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting slot: {str(e)}")