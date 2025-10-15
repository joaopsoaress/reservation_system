from backend.models import Slot
from pydantic import BaseModel

from backend.schemas import SlotCreate

async def get_slots():
    return await Slot.all()

async def get_slot(slot_id):
    return await Slot.get(id=slot_id)

async def create_slot(slot: SlotCreate):
    # Converts date to string in ISO format if it's a date object
    slot_data = slot.dict()
    slot_data['date'] = slot_data['date'].isoformat() if hasattr(slot_data['date'], 'is' \
    'oformat') else slot_data['date']

    new_slot = await Slot.create(**slot_data, status='available')
    return new_slot

async def reserve_slot(slot_id):
    slot = await Slot.get(id=slot_id)
    if slot.status == 'available':
        slot.status = 'reserved'
        await slot.save()
        return slot
    return None

async def update_slot(slot_id: int, **kwargs):
    # Converts date to string if present
    if 'date' in kwargs and hasattr(kwargs['date'], 'isoformat'):
        kwargs['date'] = kwargs['date'].isoformat()

    await Slot.filter(id=slot_id).update(**kwargs)
    return await Slot.get(id=slot_id)

async def delete_slot(slot_id):
    deleted_count = await Slot.filter(id=slot_id).delete()
    return {"deleted": deleted_count}