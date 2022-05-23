import json
from web3 import Web3

# add your blockchain connection information
infura_url = 'https://mainnet.infura.io/v3/584fdf9b4a15422fa39b2b0cad4f5197'
web3 = Web3(Web3.HTTPProvider(infura_url))


def get_ts_from_block(block_no):
  return web3.eth.getBlock(block_no)

