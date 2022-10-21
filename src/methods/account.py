from src.sql.models import User
from src.sql.connection import async_session
from sqlalchemy.future import select
from src.sql.models import Token
import sqlalchemy as sa


async def async_check_users(name):
    """Get user information func"""
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.username == name))
            for a in result.scalars().unique():
                return {
                    "id": a.id,
                    "password": a.password,
                    "rule_level": a.rule_level,
                    "activated": a.activated,
                }

    return False


async def async_get_users(user_id):
    """Show user information func"""
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.id == user_id))
            for a in result.scalars().unique():
                return {"id": a.id,
                        "username": a.username,
                        "rule_level": a.rule_level,
                        "activated": a.activated,
                        "partner_id": a.partner_id,
                        "email": a.email
                        }
    return False


async def async_check_user_tokens(token):
    """Check token's availability for user"""
    async with async_session() as session:
        async with session.begin():
            result_one = await session.execute(
                select(Token).where(Token.token == token)
            )
            for item in result_one.scalars().unique():
                return True
    return False


async def async_insert_user(user_data):
    """Add new user func"""
    async with async_session() as session:
        async with session.begin():
            await session.execute(sa.insert(User).values(user_data))
            await session.commit()
    return True
