from src.database.models import User
from tortoise.transactions import atomic


async def get_users_service():
    users_data = await User.all()
    result = [{'user_id': entry.user_id} for entry in users_data]
    return result


@atomic()
async def get_or_create_user_service(user_id: int):
    user_data = await User.get_or_none(user_id=user_id)
    if user_data is None:
        user_data = await User.create(user_id=user_id)

    return {'user_id': user_data.user_id}
