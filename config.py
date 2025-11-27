import os

DATABASE = os.getenv(
    "DATABASE", "postgresql+asyncpg://postgres:z1SJm3mUVU@localhost:55533/postgres"
)
SYNC_DATABASE = os.getenv(
    "SYNC_DATABASE", "postgresql://postgres:z1SJm3mUVU@localhost:55533/postgres"
)

TEST_DATABASE = os.getenv(
    "TEST_DATABASE", "postgresql+asyncpg://postgres:z1SJm3mUVU@localhost:55533/test_db"
)
TEST_SYNC_DATABASE = os.getenv(
    "TEST_SYNC_DATABASE", "postgresql://postgres:z1SJm3mUVU@localhost:55533/test_db"
)
NUM_OF_LAST_FIELDS = os.getenv("NUM_OF_LAST_FIELDS", 5)
