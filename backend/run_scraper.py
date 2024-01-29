import sys
from scraper.main import main
from scraper.main import DROM
import asyncio

if __name__ == '__main__':
    # Extract command-line arguments
    if len(sys.argv) < 3:
        print('Usage: python -m package_name url search_text endpoint page_count')
        sys.exit(1)

    url = sys.argv[1]
    search_text = sys.argv[2]
    endpoint = sys.argv[3]
    page_count = int(sys.argv[4])

    # Run the scraper asynchronously
    asyncio.run(main(url, search_text, endpoint, page_count))