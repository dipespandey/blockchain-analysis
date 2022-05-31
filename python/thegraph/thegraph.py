import requests
# pretty print is used to print the output in the console in an easy to read format
from pprint import pprint


uniswapV2url = 'https://api.thegraph.com/subgraphs/name/ianlapham/uniswapv2'


queryToken = """
{
  token(id: "%s"){
   name
   symbol
   decimals
   derivedETH
   tradeVolumeUSD
   totalLiquidity
   txCount
   totalSupply
 }
}
"""

queryPair = """
{
  pair(id: "%s"){
   volumeUSD
   totalSupply
   txCount
   createdAtTimestamp
 }
}
"""

def get_token_info_by_address(address):
  address = address.lower()
  # endpoint where you are making the request
  request = requests.post(uniswapV2url,
                          '',
                          json={'query': queryToken%address})
  if request.status_code == 200:
      return request.json()
  else:
      raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, queryToken))


def get_pair_info_by_address(address):
  address = address.lower()

