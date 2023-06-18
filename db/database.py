from motor.motor_asyncio import AsyncIOMotorClient


class Database:
  client = AsyncIOMotorClient('mongodb+srv://ndongo:a9125844@cluster0.ixyfun2.mongodb.net/test?retryWrites=true&w=majority')

  db=client.Cluster0