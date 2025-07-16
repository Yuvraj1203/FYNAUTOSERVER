from beanie import init_beanie
from fynautoserver.config.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from fynautoserver.schemas.index import TenantInfoSchema , AddTenantSchema,Fonts,Color

async def init_db():
    try:
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        database = client.get_database('fyn_automation')
        # Initialize Beanie with the database and models
        await init_beanie(database,document_models=[TenantInfoSchema,AddTenantSchema,Fonts,Color])
        print("the connection has been eshtablished with database fyn_automation")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise