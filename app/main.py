from fastapi import FastAPI
from app.dependencies import get_data
from scraper.scraper import run
from selenium.common.exceptions import WebDriverException

app = FastAPI(title='Drom')

@app.get('/')
async def index():
    return get_data()

@app.post('/run-scraper')
def run_scraper(pages_count: int):
    try:
        run(pages_count)
    except WebDriverException:
        return 'Something wrog with the WebDriver'
    return "Scraped succesfully!"


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', reload=True)