# import the following dependencies
import json
import time
import decimal
import datetime
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.contract import Contract
from db import dbutils, database
from w3utils import block



infura_url = 'https://speedy-nodes-nyc.moralis.io/8bddf8c916e361615f5bd7aa/bsc/mainnet/archive'
web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# add your blockchain connection information
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

def main():
    block_start = 7600899
    block_end = 7601500
    for b in range(block_start, block_end):
      onetoken = web3.toWei(1, 'ether')
      pathtosell = contract.functions.getAmountsOut(onetoken, [ETH_ADDR, USDT_ADDR]).call(block_identifier=b)
      amount = web3.fromWei(int(pathtosell[1]), 'ether') * decimal.Decimal(10E11)
      ts = block.get_block_timestamp_from_block(web3, b)
      time = datetime.datetime.fromtimestamp(ts)
      print(b, time, amount)	
			
      with open('pricesnew1.csv', 'a') as f:
          f.write(f"\n{str(round(amount, 2))},{time},Pancakeswap,smart contract")


if __name__ == '__main__':
    main()
