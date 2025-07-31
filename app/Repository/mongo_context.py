import os
from dotenv import load_dotenv
from beanie import init_beanie
import motor.motor_asyncio

from app.Models import Article

load_dotenv()

async def Initializing_Mongo_DB():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("DOCKER_INTERNAL_MONGO_URI"))
    await init_beanie(database=client[os.getenv("MONGO_DB")], document_models=[Article])