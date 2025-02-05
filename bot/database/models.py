from tortoise import fields
from tortoise.models import Model
from datetime import datetime

class BaseORM(Model):
    class Meta:
        abstract = True

    id: int = fields.IntField(pk=True)
    created_at: datetime.datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime.datetime = fields.DatetimeField(auto_now=True)


class User(BaseORM): # Для пользователей
    user_id = fields.BigIntField(pk=True)
