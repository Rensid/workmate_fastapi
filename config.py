import os

DATABASE = os.getenv(
    "DATABASE", "postgresql+asyncpg://postgres:z1SJm3mUVU@localhost:55533/postgres"
)
SYNC_DATABASE = os.getenv(
    "SYNC_DATABASE", "postgresql://postgres:z1SJm3mUVU@localhost:55533/postgres"
)
