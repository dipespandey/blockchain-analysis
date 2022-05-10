import pyppeteer
import datetime
import asyncio
from sqlalchemy.orm.session import Session
from db import database, dbutils

fromXpath = '//*[@id="swap-currency-input"]/div/div[1]/input'
toButton = '//*[@id="swap-currency-output"]/div/div/button'
usdtButton = '//img[@alt="USDT logo"]'
outputField = '//*[@id="swap-currency-output"]/div/div[1]/input'

url = 'https://app.uniswap.org'
async def main():
    browser = await pyppeteer.launch()
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
    
    start_time = datetime.datetime.strptime('2022-04-06 10:35:00', '%Y-%m-%d %H:%M:%S')\
        .replace(tzinfo=datetime.timezone.utc)
    end_time = datetime.datetime.strptime('2022-04-06 10:40:00', '%Y-%m-%d %H:%M:%S')\
        .replace(tzinfo=datetime.timezone.utc)
    
    session: Session = database.create_connection()

    while True:
        current_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        if current_time > end_time:
            break
        elif current_time >= start_time:
            output = await page.xpath(outputField)
            price = await output[0].getProperty('value')
            p = price._remoteObject.get('value')
            await page.waitFor(10000)
            all_prices = dbutils.get_all(session)
            ts = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            if ts not in [i.ts for i in all_prices if i.source == 'Uniswap']:
                dbutils.write_row(session, {'price': str(p), 'source': 'Uniswap', 'ts': str(ts)})

asyncio.get_event_loop().run_until_complete(main())


