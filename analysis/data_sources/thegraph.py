from gql import gql, Client
from typing import Any, Dict, Optional
from gql.transport.requests import RequestsHTTPTransport



class GraphAPI:
    def __init__(self, exchange):
        self.exchange = exchange
        self.url = 'http://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
        
        transport = RequestsHTTPTransport(
            url=self.url,
            retries=3,
        )
        self.client = Client(transport=transport)

    def query(self, query):
        query = gql(query)
        return self.client.execute(query)

    def get_all_pairs(self):
        if self.exchange == 'uniswap':
            query_root = 'swaps'
        else:
            query_root = 'pairs'
        all_pairs = []
        timestamp = 1609459200
        while True:
            query = """
                { 
                    %s (first: 1000, where: {id_gt: "%s"}, orderBy: timestamp) 
                {   
                    id
                    timestamp
                    amountUSD
                    token0 {
                        symbol
                        name
                    }
                    token1 {
                        symbol 
                        name
                    }
                }
                }
            """ % (query_root, timestamp)
            print(query)
            query = gql(query)
            pairs = self.client.execute(query).get(query_root)
            if len(pairs) == 0:
                break
            else:
                print('printing\n\n\n')
                print(len(all_pairs), pairs[-1]['timestamp'])
            
                timestamp = pairs[-1]['timestamp']
                all_pairs.extend(pairs)
        return all_pairs

    def get_transactions_for_a_pair(self, pair_id):
        pass

    def __str__(self):
        return f'TheGraph API for {self.exchange}' 
    
    def __repr__(self):
        return f'TheGraph API for {self.exchange}' 


def get_all_pairs(exchange):
    g = GraphAPI(exchange)
    r = g.get_all_pairs()
    print(r)