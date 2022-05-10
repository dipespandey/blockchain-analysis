# import the following dependencies
import json
from web3 import Web3
from web3.contract import Contract
import asyncio

# add your blockchain connection information
infura_url = 'https://mainnet.infura.io/v3/584fdf9b4a15422fa39b2b0cad4f5197'
web3:Web3 = Web3(Web3.HTTPProvider(infura_url))

PAIR_ADDR = web3.toChecksumAddress("0xa478c2975ab1ea89e8196811f51a7b7ade33eb11")
PAIR_NAME = "WETH/USDT"
WETH_ADDR = web3.toChecksumAddress('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
USDT_ADDR = web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')
INTERVAL = 1000

# uniswap address and abi
uniswap_router = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
uniswap_factory = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
uniswap_router_str = open('../abi/uniswapv2router.json')
uniswap_router_abi = json.load(uniswap_router_str)
contract: Contract = web3.eth.contract(address=web3.toChecksumAddress(uniswap_router), abi=uniswap_router_abi)

# weth_abi = json.load(open('../abi/WETH.json'))
# contract: Contract = web3.eth.contract(address=web3.toChecksumAddress(WETH_ADDR), abi=weth_abi)

def handle_event(event):
    print(Web3.toJSON(event))

async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)

def watch_sync():
    event_filter = contract.events.Sync.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()

# sellTokenContract = web3.eth.contract(WETH_ADDR, abi=weth_abi)

def main():
    start = 10008555
    end = 14557640
    for i in range(start, end+1):
        try:
            pathtosell = contract.functions.getAmountsOut(1000000000000000000, 
            [WETH_ADDR, USDT_ADDR]).call(block_identifier=i)
            print(i,pathtosell[-1])
        except Exception as e:
            print(i, 'Trie Exception')
    # amount = web3.fromWei(pathtosell[len(pathtosell)-1], 'ether')
    # for i in contract.all_functions():
    #     print(i,)
    # print([i for i in contract.all_functions()])

def get_txns_by_account(router_addr):
    start = 10008555
    end = 14557640
    count = 0
    for i in range(start, start+100):
        block = web3.eth.getBlock(i)
        if block is not None and block.transactions is not None:
            for j in block.transactions:
                tx = web3.eth.getTransaction(j)
                if tx.to and (tx.to.lower() == router_addr.lower() or tx['from'].lower() == router_addr.lower()):
                    print(tx)
            count += len(block.transactions)
            print(count)
    

if __name__ == "__main__":
    get_txns_by_account('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D') #uniswapV2