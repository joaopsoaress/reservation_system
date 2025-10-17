from backend.models import Slot
from pydantic import BaseModel

from backend.schemas import SlotCreate

    # Function that lists all slots
async def get_slots():
    return await Slot.all()

    # Function that gets a specific slot by ID
async def get_slot(slot_id):
    return await Slot.get(id=slot_id)

    # Function that creates a new slot
async def create_slot(slot: SlotCreate):
    # Converts date to string in ISO format if it's a date object
    slot_data = slot.dict()
    slot_data['date'] = slot_data['date'].isoformat() if hasattr(slot_data['date'], 'is' \
    'oformat') else slot_data['date']

    new_slot = await Slot.create(**slot_data, status='available')
    return new_slot

    # Function that reserves a slot if it's available
async def reserve_slot(slot_id):
    slot = await Slot.get(id=slot_id)
    if slot.status == 'available':
        slot.status = 'reserved'
        await slot.save()
        return slot
    return None

    # Function that updates a slot
async def update_slot(slot_id: int, **kwargs):
    # Converts date to string if present
    if 'date' in kwargs and hasattr(kwargs['date'], 'isoformat'):
        kwargs['date'] = kwargs['date'].isoformat()

    await Slot.filter(id=slot_id).update(**kwargs)
    return await Slot.get(id=slot_id)

    # Function that deletes a slot
async def delete_slot(slot_id):
    deleted_count = await Slot.filter(id=slot_id).delete()
    return {"deleted": deleted_count}