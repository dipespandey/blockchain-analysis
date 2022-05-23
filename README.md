# Crypto Exchange Compare

This repo contains the code used for the thesis: 

These experiments are performed:
1. Watch a smart contract(Uniswap V2 and Pancakeswap)
  a. save the transactions/pairs/tokens into database
2. Use third party tools to get blockchain data
  a. The Graph
3. Scrape Google Scholar to perform Systematic Literature Review
4. Get data from Binance API
5. Scrape prices from Uniswap and Pancakeswap official web interface


$ docker build -t exchange .
docker run -e MYSQL_ROOT_PASSWORD=pw -p 3306:3306 exchange
