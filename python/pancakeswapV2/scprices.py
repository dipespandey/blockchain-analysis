# import the following dependencies
import json
import time
import decimal
import datetime
from web3 import Web3
from sqlalchemy.orm import Session
from web3.contract import Contract
from db import database, dbutils

infura_url = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(infura_url))

PAIR_ADDR = web3.toChecksumAddress("0xEa26B78255Df2bBC31C1eBf60010D78670185bD0")
PAIR_NAME = "ETH/USDT"
ETH_ADDR = web3.toChecksumAddress('0x2170ed0880ac9a755fd29b2688956bd959f933f8')
USDT_ADDR = web3.toChecksumAddress('0x55d398326f99059fF775485246999027B3197955')
INTERVAL = 1000

# pancakeswap address and abi
pancakeswap_router = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
pancakeswap_factory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
pancakeswap_router_str = open('abi/pancakeswapv2router.json')
pancakeswap_router_abi = json.load(pancakeswap_router_str)
contract: Contract = web3.eth.contract(address=web3.toChecksumAddress(pancakeswap_router), abi=pancakeswap_router_abi)


def handle_event(event, session):
    print('new block detected ...')
    print(Web3.toJSON(event))
    try:
        onetoken = web3.toWei(1, 'ether')
        print(onetoken)
        pathtosell = contract.functions.getAmountsOut(onetoken, [ETH_ADDR, USDT_ADDR]).call()
        amount = web3.fromWei(int(pathtosell[1]), 'ether') * decimal.Decimal(10E11)
        ts = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        all_prices = dbutils.get_all_prices(session)
        if ts not in [i.ts for i in all_prices if i.source == 'Pancakeswap']:
            dbutils.write_price_row(session, {'price': str(round(amount, 2)), 'exchange': 'Pancakeswap', 
            'source': 'smart contract', 'ts': str(ts)})
        with open('pricesnew.csv', 'a') as f:
            f.write(f"\n{str(round(amount, 2))},{ts},Pancakeswap,smart contract")
    except Exception as e:
        print(e)


def log_loop(event_filter, poll_interval, session):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event, session)
        time.sleep(poll_interval)


def main(session):
    block_filter = web3.eth.filter('latest')
    log_loop(block_filter, 2, session)

if __name__ == '__main__':
    session = database.create_connection()
    main(session)
