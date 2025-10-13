from backend.database import Slot
from pydantic import BaseModel

from backend.schemas import SlotCreate

async def get_slots():
    return await Slot.all()

async def get_slot(slot_id):
    return await Slot.get(id=slot_id)

async def create_slot(slot: SlotCreate):
    new_slot = await Slot.create(**slot.dict())
    return new_slot

async def reserve_slot(slot_id):
    return await Slot.filter(id=slot_id).update(status='reserved')

async def update_slot(slot_id, **kwargs):
    return await Slot.filter(id=slot_id).update(**kwargs)

async def delete_slot(slot_id):
    return await Slot.filter(id=slot_id).delete()