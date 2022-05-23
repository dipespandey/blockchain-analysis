from concurrent.futures import ProcessPoolExecutor
import functools  # at the top with the other imports
import asyncio
from multiprocessing import Process, Manager
from db import database
from pancakeswapV2 import scraper as pscraper
from pancakeswapV2 import scprices as pscprices
from uniswapV2 import scraper as uscraper
from uniswapV2 import scprices as uscprices

session = database.create_connection()


def one():
    pscprices.main(session=session)
  
def two():
    uscprices.main(session=session)

# '2022-05-22 21:48:00'
if __name__ == '__main__':

  executor = ProcessPoolExecutor(2)
  loop = asyncio.get_event_loop()
  loop.run_in_executor(executor, one)
  loop.run_in_executor(executor, two)
  # loop.run_in_executor(None, foo)
  # loop.run_in_executor(executor, lambda: uscraper.mainf(session=session, start='2022-0-22 20:50:00', end='2022-0-22 20:50:00'))

  loop.run_forever()