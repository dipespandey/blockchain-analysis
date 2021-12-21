# blockchain-analysis

Use the public blockchain data to infer insights


## Schema of the dataset
** is taken from [https://github.com/blockchain-etl/ethereum-etl/edit/develop/docs/schema.md](https://github.com/blockchain-etl/ethereum-etl/edit/develop/docs/schema.md)


### The following files are used

1. analysis/data_sources/pricing.py -> get the pricing data from Binance and CoinPaprika API
2. analysis/data_sources/thegraph.py -> use The Graph API to get blockchain data from subgraphs
3. analysis/data_sources/thegraph.py -> get data by directly querying the smart contract
4. analysis/utils.py -> get additional data by scraping the Etherscan website

