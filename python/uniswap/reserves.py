# import the following dependencies
import json
import time
from web3 import Web3
from web3.contract import Contract
import asyncio

# add your blockchain connection information
infura_url = 'https://mainnet.infura.io/v3/584fdf9b4a15422fa39b2b0cad4f5197'
web3 = Web3(Web3.HTTPProvider(infura_url))

PAIR_ADDR = web3.toChecksumAddress("0xa478c2975ab1ea89e8196811f51a7b7ade33eb11")
PAIR_NAME = "WETH/USDT"
WETH_ADDR = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
USDT_ADDR = '0xdac17f958d2ee523a2206206994597c13d831ec7'
INTERVAL = 1000

# uniswap address and abi
uniswap_router = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
uniswap_factory = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
uniswap_pair_str = open('../abi/IUniswapV2Pair.json')
uniswap_pair_abi = json.load(uniswap_pair_str)
pair_contract: Contract = web3.eth.contract(address=PAIR_ADDR, abi=uniswap_pair_abi['abi'])

def handle_event(event):
    print(Web3.toJSON(event))

async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)

def watch_sync():
    event_filter = pair_contract.events.Sync.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()

def main():
    token0reserve, token1reserve, _ = pair_contract.functions.getReserves().call()
    print(token0reserve, token1reserve)
    # temp = token0reserve/token1reserve
    # print(temp)
    # result = temp - 0.3/100*temp
    # print(result)
    token0reserve = float(token0reserve)/(10**18)
    token1reserve = float(token1reserve)/(10**18)
    constant_product = token0reserve*token1reserve
    
    new_token1_reserve = constant_product/token0reserve
    print(new_token1_reserve)
    token1out = token1reserve-new_token1_reserve
    print(token1out)

if __name__ == "__main__":
    for i in range(10):
        main()
        time.sleep(15)