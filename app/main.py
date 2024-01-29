from fastapi import FastAPI
from app.dependencies import get_data
from scraper.main import main
from selenium.common.exceptions import WebDriverException

app = FastAPI(title='Drom')

@app.get('/')
async def index():
    return get_data()

@app.post('/add-tracked-product')
async def add_tracked_product(name: str):
    pass

@app.post('/run-scraper')
async def run_scraper(url, search_text: str):
    try:
        await main(url, search_text)
    except WebDriverException:
        return 'Something wrog with the WebDriver'
    return "Scraped succesfully!"


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', reload=True)