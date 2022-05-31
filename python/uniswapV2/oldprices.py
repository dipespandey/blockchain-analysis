# import the following dependencies
import json
import time
import decimal
import datetime
from web3 import Web3
from web3.contract import Contract
from db import dbutils, database
from w3utils import block

# add your blockchain connection information
local_url = 'http://eth.dse.ntnu.no:8545'
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


def main():
    block_start = 12474190
    block_end = 12484190
    for b in range(block_start, block_end):
      onetoken = web3.toWei(1, 'ether')
      pathtosell = contract.functions.getAmountsOut(onetoken, [WETH_ADDR, USDT_ADDR]).call(block_identifier=b)
      amount = web3.fromWei(int(pathtosell[1]), 'ether') * decimal.Decimal(10E11)
      ts = block.get_block_timestamp_from_block(web3, b)
      time = datetime.datetime.fromtimestamp(ts)
      print(b, time, amount)

      with open('pricesnew.csv', 'a') as f:
          f.write(f"\n{str(round(amount, 2))},{time},Uniswap,smart contract")


if __name__ == '__main__':
    main()
