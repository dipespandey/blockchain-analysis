# import the following dependencies
import json
import asyncio
import datetime
from web3 import Web3
from sqlalchemy.orm import Session
from db import database, dbutils
from w3utils import block, token


# add your blockchain connection information
infura_url = 'https://bsc-dataseed1.binance.org:443'
web3 = Web3(Web3.HTTPProvider(infura_url))

# uniswap address and abi
pancake_router = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
pancake_factory = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
pancake_factory_abi = json.loads(open('abi/pancakeswapv2router.json'))

contract = web3.eth.contract(address=pancake_factory, abi=pancake_factory_abi)


def handle_event(event):
    print(Web3.toJSON(event))
    pair = str(Web3.toJSON(event))
    ts = block.get_ts_from_block(pair['blockNumber'])
    token0 = token.get_token_info_from_address(pair['args']['token0'])

    token1 = token.get_token_info_from_address(pair['args']['token1'])
    ts = datetime.datetime.from_timestamp(ts).replace(tzinfo=datetime.timezone.utc)
    session: Session = database.create_connection()
    # get token info
    # get txn time
    dbutils.write_pair_row(session, {
        'token0address': pair['args']['token0'], 
        'token1address': pair['args']['token0'], 
        'pairaddress': pair['args']['pair'],
        'token0symbol': token0['symbol'],
        'token1symbol': token1['symbol'],
        'created_at': ts })

# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.PairCreated.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
    main()