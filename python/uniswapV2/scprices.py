# import the following dependencies
import json
import time
import decimal
import datetime
from web3 import Web3
from web3.contract import Contract
from db import dbutils, database

# add your blockchain connection information
local_url = 'https://mainnet.infura.io/v3/584fdf9b4a15422fa39b2b0cad4f5197'
web3 = Web3(Web3.HTTPProvider(local_url))

PAIR_ADDR = web3.toChecksumAddress("0xa478c2975ab1ea89e8196811f51a7b7ade33eb11")
PAIR_NAME = "WETH/USDT"
WETH_ADDR = web3.toChecksumAddress('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
USDT_ADDR = web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
INTERVAL = 1000

# uniswap address and abi
uniswap_router = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
uniswap_factory = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
uniswap_router_str = open('abi/uniswapv2router.json')
uniswap_router_abi = json.load(uniswap_router_str)
contract: Contract = web3.eth.contract(address=web3.toChecksumAddress(uniswap_router), abi=uniswap_router_abi)


def handle_event(event, session):
    print('new block detected ...')
    print(Web3.toJSON(event))
    try:
        onetoken = web3.toWei(1, 'ether')
        print(onetoken)
        pathtosell = contract.functions.getAmountsOut(onetoken, [WETH_ADDR, USDT_ADDR]).call()
        amount = web3.fromWei(int(pathtosell[1]), 'ether') * decimal.Decimal(10E11)
        ts = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        
        # all_prices = dbutils.get_all_prices(session)
        print(amount)
        # if ts not in [i.ts for i in all_prices if i.source == 'Uniswap']:
            # dbutils.write_price_row(session, {'price': str(round(amount, 2)), 'exchange': 'Uniswap', 
            # 'source': 'smart contract', 'ts': str(ts)})  
        with open('prices.csv', 'a') as f:
            f.write(f"\n{str(round(amount, 2))},{ts},Uniswap,smart contract")
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
    # session = database.create_connection()
    main(None)
