from app import app
from app.dependencies import get_data
from scraper.main import main
from selenium.common.exceptions import WebDriverException
from web_app.app.products.router import router as product_router
import subprocess


app.include_router(product_router)

@app.post('/run-scraper')
async def run_scraper(url: str, search_text: str, page_count: int = 10):
    try:
        command = f"python ./run_scraper.py {url} \"{search_text}\" /products/results {page_count}"
        subprocess.Popen(command, shell=True)
    except WebDriverException:
        return 'Something wrog with the WebDriver'
    response = {'message': 'Scraper started successfully'}
    return response
