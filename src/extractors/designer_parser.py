thonimport puppeteer
import json

async def parse_designer_profile(url):
    browser = await puppeteer.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.goto(url, waitUntil='domcontentloaded')

    designer = {}
    designer['userName'] = await page.$eval('h1.profile-name', el => el.innerText)
    designer['profileUrl'] = url
    designer['pro'] = await page.$eval('.pro-badge', el => el.innerText) if await page.$('.pro-badge') else 'Basic'
    designer['skills'] = await page.$$eval('.skill', skills => skills.map(skill => skill.innerText))
    designer['tags'] = await page.$$eval('.meta-tag', tags => tags.map(tag => tag.innerText))

    await browser.close()
    return designer