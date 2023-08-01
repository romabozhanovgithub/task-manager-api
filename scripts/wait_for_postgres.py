import os
import asyncpg
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def main():
    """
    Wait for postgres to start
    """
    while True:
        try:
            await asyncpg.connect(
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                database=os.getenv("POSTGRES_DB"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
            )
            break
        except (
            ConnectionRefusedError,
            asyncpg.exceptions.CannotConnectNowError,
        ):
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
