import json
from web3 import Web3
from web3.contract import Contract

infura_url = 'https://mainnet.infura.io/v3/584fdf9b4a15422fa39b2b0cad4f5197'
web3 = Web3(Web3.HTTPProvider(infura_url))


def get_token_info_from_address(address):
    abi_token = json.load(open('../abi/IUniswapV2Token.json'))
    token_contract: Contract = web3.eth.contract(address=address, abi=abi_token)
    symbol = token_contract.functions.symbol().call()
    decimals = token_contract.functions.decimals().call()
    name = token_contract.functions.name().call()
    return {
        'symbol': symbol,
        'decimals': decimals,
        'name': name
    }
