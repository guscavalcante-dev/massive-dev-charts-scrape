import asyncio
import httpx
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import quote_plus
from tqdm.asyncio import tqdm_asyncio
from dice import roll_dice

BASE_URL = "https://www.digitaltruth.com/devchart.php"
OUTPUT_DIR = "charts_async"
MAX_CONCURRENT_REQUESTS = 4
MAX_RETRIES = 3

os.makedirs(OUTPUT_DIR, exist_ok=True)
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def fetch(client, url, retries=MAX_RETRIES, delay=1):
    for attempt in range(retries):
        try:
            async with semaphore:
                res = await client.get(url, timeout=20.0)
                res.raise_for_status()
                return res.text
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay * 2 ** attempt)
            else:
                raise e


async def get_all_film_urls(client):
    print("🔍 Buscando lista de filmes...")
    html = await fetch(client, BASE_URL)
    soup = BeautifulSoup(html, 'html.parser')
    film_select = soup.find('select', {'name': 'Film'})
    film_urls = []

    for option in film_select.find_all('option'):
        film_value = option.get('value')
        if film_value and film_value.lower() != 'all':
            film_name = option.text.strip()
            url = f"{BASE_URL}?Film={quote_plus(film_value)}&Developer=&mdc=Search&TempUnits=C&TimeUnits=T"
            film_urls.append((film_name, url))

    return film_urls


async def scrape_film_page(client, film_name, url):
    try:
        html = await fetch(client, url)
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', {'class': 'mdctable'})

        if not table:
            return

        data = []
        rows = table.find_all('tr')[1:]

        for row in rows:
            cols = [td.text.strip() for td in row.find_all('td')]
            if len(cols) >= 5:
                entry = {
                    "film": film_name,
                    "developer": cols[0],
                    "dilution": cols[1],
                    "time": cols[2],
                    "temperature": cols[3],
                    "agitation": cols[4],
                }
                data.append(entry)

        if data:
            filename = os.path.join(
                OUTPUT_DIR,
                f"{film_name.replace(' ', '_').replace('/', '_')}.json"
            )
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"❌ Erro em {film_name}: {e}")


async def main():
    roll_dice()
    async with httpx.AsyncClient(http2=True) as client:
        film_urls = await get_all_film_urls(client)
        print(f"🎞️ {len(film_urls)} filmes encontrados.\n")

        tasks = [
            scrape_film_page(client, film_name, url)
            for film_name, url in film_urls
        ]

        await tqdm_asyncio.gather(*tasks, desc="⏳ Processando filmes")


if __name__ == "__main__":
    asyncio.run(main())
