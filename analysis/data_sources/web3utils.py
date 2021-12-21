from web3 import Web3
from abis import pancake_pair_abi, contract_abi

BSC_P_URL = 'https://bsc-dataseed.binance.org/'
UNI_URL = ''
# extract pairs from 
w3 = Web3(Web3.HTTPProvider(BSC_P_URL))


def get_transaction_data(provider_url, txn_hash):
    return w3.eth.getTransaction(txn_hash)
    

def get_factory_contract(address):
    return w3.eth.contract(address=address, abi=contract_abi)


def get_pair_info(factory_contract):
    all_pairs_length = factory_contract.functions.allPairsLength().call()
    for i in range(all_pairs_length):
        pair_abi = pancake_pair_abi
        pair = factory_contract.functions.allPairs(i).call()
        pair_contract = w3.eth.contract(address=pair, abi=pair_abi)
        print({
            'decimals': pair_contract.functions.decimals().call(),
            'reserves': pair_contract.functions.getReserves().call(),
            'name': pair_contract.functions.name().call(),
            'totalSupply': pair_contract.functions.totalSupply().call(),
        })
        if i == 10:
                break


# def get_token_from_id(id):
#     w3.eth.acc

factory_contract = get_factory_contract('0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73')
get_pair_info(factory_contract)
