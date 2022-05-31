import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

# add your blockchain connection information
bsc_url = 'https://bsc-dataseed.binance.org/'
eth_url = 'http://eth.dse.ntnu.no:8545'
# web3 = Web3(Web3.HTTPProvider(infura_url))
# web3.middleware_onion.inject(geth_poa_middleware, layer=0)

def create_w3_client(url):
  web3 = Web3(Web3.HTTPProvider(url))
  if 'bsc' in url:
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
  return web3


def get_txn_info_from_block(w3, tx_hash):
  return w3.eth.getTransaction(tx_hash).timestamp


def get_block_timestamp_from_block(w3, block):
  return w3.eth.getBlock(block).timestamp


def get_block_closest_to_timestamp(w3, ts):
  pass