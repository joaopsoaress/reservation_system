from tortoise import Tortoise, fields
from tortoise.models import Model

class Slot(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    hour = fields.TimeField()
    duration = fields.IntField()
    status = fields.CharField(max_length=21)
