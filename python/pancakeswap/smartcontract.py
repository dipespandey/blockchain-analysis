# import the following dependencies
import json
from web3 import Web3
from web3.contract import Contract
import asyncio

# add your blockchain connection information
infura_url = 'https://speedy-nodes-nyc.moralis.io/8bddf8c916e361615f5bd7aa/bsc/mainnet/archive'
web3 = Web3(Web3.HTTPProvider(infura_url))

PAIR_ADDR = web3.toChecksumAddress("0xEa26B78255Df2bBC31C1eBf60010D78670185bD0")
PAIR_NAME = "ETH/USDC"
ETH_ADDR = web3.toChecksumAddress('0x2170ed0880ac9a755fd29b2688956bd959f933f8')
USDC_ADDR = web3.toChecksumAddress('0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d')
INTERVAL = 1000

# pancakeswap address and abi
pancakeswap_router = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
pancakeswap_factory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
pancakeswap_router_str = open('../abi/pancakeswapv2router.json')
pancakeswap_router_abi = json.load(pancakeswap_router_str)
contract: Contract = web3.eth.contract(address=web3.toChecksumAddress(pancakeswap_router), abi=pancakeswap_router_abi)

# weth_abi = json.load(open('../abi/WETH.json'))
# contract: Contract = web3.eth.contract(address=web3.toChecksumAddress(WETH_ADDR), abi=weth_abi)

# def handle_event(event):
#     print(Web3.toJSON(event))

# async def log_loop(event_filter, poll_interval):
#     while True:
#         for PairCreated in event_filter.get_new_entries():
#             handle_event(PairCreated)
#         await asyncio.sleep(poll_interval)

# def main():
#     event_filter = contract.events.Sync.createFilter(fromBlock='latest')
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(
#             asyncio.gather(
#                 log_loop(event_filter, 2)))
#     finally:
#         # close loop to free up system resources
#         loop.close()
# sellTokenContract = web3.eth.contract(WETH_ADDR, abi=weth_abi)

def main():
    start = 16856678-100
    end = 16856678
    for i in range(start, end+1):
        try:
            pathtosell = contract.functions.getAmountsOut(1000000000000000000, [ETH_ADDR, USDC_ADDR]).call(block_identifier=i)
            print(i,pathtosell[-1])
        except Exception as e:  
            print(e, i, 'Trie Exception')
    # amount = web3.fromWei(pathtosell[len(pathtosell)-1], 'ether')
    # for i in contract.all_functions():
    #     print(i,)
    # print([i for i in contract.all_functions()])

if __name__ == "__main__":
    main()