import asyncio
from src.db.setup import init_models

def main():
    asyncio.run(init_models())


if __name__ == "__main__":
    main()
    