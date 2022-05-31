import time
import pyppeteer
import datetime
import asyncio
from sqlalchemy.orm.session import Session
from db import database, dbutils

fromButtonXpath = '//*[@id="swap-currency-input"]/div[1]/div/button'
searchInputXpath = '//*[@id="token-search-input"]'
ethButtonXpath = '//div/img[@alt="ETH logo"]'
inputField = '//*[@id="swap-currency-input"]/div[2]/label/div[1]/input'
toButtonXpath = '//*[@id="swap-currency-output"]/div[1]/div/button'
searchOutputXpath = '//*[@id="token-search-input"]'
usdtButton = '//div/img[@alt="USDT logo"]'
closeDialogButton = '//button[@aria-label="Close the dialog"]'
outputField = '//*[@id="swap-currency-output"]/div[2]/label/div[1]/input'

url = 'https://pancakeswap.finance/swap'


async def main(session, start, end):
    browser = await pyppeteer.launch()
    page = await browser.newPage()

    await page.goto(url)
    await page.waitFor(3000)
    fromButton = await page.xpath(fromButtonXpath)
    await fromButton[0].click()
    await page.waitFor(2000)

    searchEl = await page.xpath(searchInputXpath)
    await searchEl[0].type('ETH')
    await page.waitFor(2000)

    ethButton = await page.xpath(ethButtonXpath)
    await ethButton[0].click()
    await page.waitFor(2000)

    fromEl = await page.xpath(inputField)
    await fromEl[0].type('1')
    await page.waitFor(2000)

    to = await page.xpath(toButtonXpath)
    await to[0].click()
    await page.waitFor(4000)

    searchEl = await page.xpath(searchOutputXpath)
    await searchEl[0].type('USDT')
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
            new = await output[0].getProperty('value')
            newval = new._remoteObject.get('value')
            all_prices = dbutils.get_all_prices(session)
            ts = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            if ts not in [i.ts for i in all_prices if i.source == 'Pancakeswap']:
                dbutils.write_price_row(session, {'price': str(newval), 'ts': str(ts), 
                'exchange': 'Pancakeswap', 'source': 'scraper'})
            with open('prices.csv', 'a') as f:
                f.write(f"\n{str(newval)},{ts},Pancakeswap,scraper")
            time.sleep(10000)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main(None, '2022-05-23 06:35:00', '2022-06-20 08:35:00'))