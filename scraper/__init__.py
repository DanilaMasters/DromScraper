from scraper.main import main
from scraper.main import DROM
import asyncio

if __name__ == "__main__":
    # test script
    asyncio.run(main(DROM, "toyota"))