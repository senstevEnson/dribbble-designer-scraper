thonimport puppeteer
import json
import time
from extractors.designer_parser import parse_designer_profile
from config.settings import MAX_RESULTS

async def scrape_dribbble(keyword):
    browser = await puppeteer.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.goto(f"https://dribbble.com/search/{keyword}", waitUntil='domcontentloaded')

    designers = []
    while len(designers) < MAX_RESULTS:
        profiles = await page.$$eval('.dribbble-profile', elements => elements.map(el => el.href))
        for profile in profiles:
            designer_data = await parse_designer_profile(profile)
            designers.append(designer_data)
            if len(designers) >= MAX_RESULTS:
                break

        next_button = await page.$('a.next_page')
        if next_button:
            await next_button.click()
            time.sleep(2)
        else:
            break

    await browser.close()
    return designers

if __name__ == '__main__':
    keyword = 'UI/UX Designer'
    designers = scrape_dribbble(keyword)
    with open('output.json', 'w') as f:
        json.dump(designers, f, indent=4)