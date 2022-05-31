import time
import pyppeteer
import datetime
import asyncio
from sqlalchemy.orm.session import Session
from db import database, dbutils


fromXpath = '//*[@id="swap-currency-input"]/div/div[1]/input'
toButton = '//*[@id="swap-currency-output"]/div/div/button'
usdtButton = '//img[@alt="USDT logo"]'
outputField = '//*[@id="swap-currency-output"]/div/div[1]/input'
feeField = ''
url = 'https://app.uniswap.org?use=v2'


async def main(session, start, end):
    browser = await pyppeteer.launch(headless=False)
    page = await browser.newPage()

    await page.goto(url)

    fromEl = await page.xpath(fromXpath)
    await fromEl[0].type('1')
    await page.waitFor(1000)
    
    to = await page.xpath(toButton)
    await to[0].click()
    await page.waitFor(2000)

    usdt = await page.xpath(usdtButton)
    await usdt[0].click()
    await page.waitFor(4000)
    
    start_time = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')\
        .replace(tzinfo=datetime.timezone.utc)
    end_time = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')\
        .replace(tzinfo=datetime.timezone.utc)
    
    while True:
        current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        if current_time > end_time:
            break
        elif current_time >= start_time:
            output = await page.xpath(outputField)
            price = await output[0].getProperty('value')
            p = price._remoteObject.get('value')
            await page.waitFor(10000)
            all_prices = dbutils.get_all_prices(session)
            ts = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            if ts not in [i.ts for i in all_prices if i.source == 'Uniswap']:
                dbutils.write_price_row(session, {'price': str(p), 'exchange': 'Uniswap', 'source': 'scraper', 'ts': str(ts)})
            with open('prices.csv', 'a') as f:
                f.write(f"\n{str(p)},{ts},Uniswap,scraper")
            time.sleep(10000)

if __name__ == '__main__':
    session = database.create_connection()
    asyncio.get_event_loop().run_until_complete(main(None, '2022-05-23 06:35:00', '2022-06-20 08:35:00'))