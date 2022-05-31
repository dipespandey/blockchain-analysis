# import the following dependencies
import json
import time
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
uniswap_router_abi = json.load(open('abi/uniswapv2router.json'))
contract: Contract = web3.eth.contract(address=web3.toChecksumAddress(uniswap_router), abi=uniswap_router_abi)


def get_txns_by_account(router_addr):
    start = 11000000
    end = 12001000
    count = 0
    start_time = time.time()
    for i in range(start, end):
        print(i)
        block = web3.eth.getBlock(i)
        if block is not None and block.transactions is not None:
            for j in block.transactions:
                tx = web3.eth.getTransaction(j)
                if tx.to and (tx.to.lower() == router_addr.lower() or tx['from'].lower() == router_addr.lower()):
                    print(tx)
                    txn = str(tx)
                    with open('txns.txt', 'a') as f:
                        f.write(f'\n{txn}')
            count += len(block.transactions)
            if count >= 10000:
                break
    print('total time:', time.time() - start_time)
    print(count)

if __name__ == "__main__":
    get_txns_by_account('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D') #uniswap V2 router
