import pyppeteer
import asyncio

resultsxpath = '//div[@id="gs_res_ccl_mid"]/div'
url = 'https://scholar.google.com/scholar?q="uniswap"+AND+"data"'
tds = '//*/table/tbody/tr/td'

async def main():
    browser = await pyppeteer.launch({'headless': False})
    page = await browser.newPage()

    await page.goto(url)

    fromEl = await page.xpath(resultsxpath)
    pages = await page.xpath(tds)
    print(len(pages))
    for i in pages:
        for j in fromEl:
            title = await j.asElement().Jeval('h3', 'e => e.innerText')
            print(title)
        next_link = await i.xpath('//*/a')
        page.waitFor(2000)
        if len(next_link) > 0:
            await next_link[0].asElement().click()
            page.waitFor(5000)

asyncio.get_event_loop().run_until_complete(main())


