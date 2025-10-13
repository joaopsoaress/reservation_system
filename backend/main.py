from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from backend import models

app = FastAPI()

register_tortoise(
    app,
    db_url='sqlite://:memory:',
    modules={'models': ['backend.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

from backend.routers import slots

app.include_router(slots.router)

