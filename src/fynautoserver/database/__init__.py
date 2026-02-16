from typing import Any
from beanie import init_beanie
from fynautoserver.config.config import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fynautoserver.schemas.index import TenantInfoSchema , AddTenantSchema,Fonts,Color, UserSchema,ReleasesVersionTableSchema

async def init_db() -> None:
    try:
        client:AsyncIOMotorClient[Any] = AsyncIOMotorClient(settings.DATABASE_URL)
        database:AsyncIOMotorDatabase[Any] = client.get_database('fyn_automation')
        # Initialize Beanie with the database and models
        await init_beanie(
            database=database,document_models=[TenantInfoSchema,AddTenantSchema,Fonts,Color,UserSchema,ReleasesVersionTableSchema]
            )  # pyright: ignore[reportUnknownVariableType]
        print("the connection has been eshtablished with database fyn_automation")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise