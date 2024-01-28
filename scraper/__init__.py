from scraper import run
import asyncio

async def main():
    await run(1, 'X5')

if __name__ == "__main__":
    import tracemalloc
    tracemalloc.start()
    asyncio.run(main())