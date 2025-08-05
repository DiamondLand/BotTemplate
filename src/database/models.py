from tortoise import fields
from src.database.abstract import BaseORM


class User(BaseORM): # Для пользователей
    user_id = fields.BigIntField()
