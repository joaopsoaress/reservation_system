from tortoise import fields
from tortoise.models import Model

    # Slot model definition
class Slot(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    hour = fields.CharField(max_length=8) # Storing time as string "HH:MM:SS"
    duration = fields.IntField()
    status = fields.CharField(max_length=20, default='available')

    # Meta information
class Meta:
    table = "slots"