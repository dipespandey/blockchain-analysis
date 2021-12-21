import re
import sys
import json
import gevent
import requests
from gql import gql, Client
from typing import Any, Dict, Optional
from gql.transport.requests import RequestsHTTPTransport


GRAPH_QUERY_LIMIT = 1000
GRAPH_QUERY_SKIP_LIMIT = 5000
RE_MULTIPLE_WHITESPACE = re.compile(r'\s+')
RETRY_BACKOFF_FACTOR = 0.2
QUERY_RETRY_TIMES = 3
class RemoteError(Exception):
    pass

class Graph():

    def __init__(self, url: str) -> None:
        """
        - May raise requests.RequestException if there is a problem connecting to the subgraph"""
        transport = RequestsHTTPTransport(url=url)
        try:
            self.client = Client(transport=transport, fetch_schema_from_transport=False)
        except (requests.exceptions.RequestException) as e:
            raise RemoteError(f'Failed to connect to the graph at {url} due to {str(e)}') from e

    def query(
            self,
            querystr: str,
            param_types: Optional[Dict[str, Any]] = None,
            param_values: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Queries The Graph for a particular query
        May raise:
        - RemoteError: If there is a problem querying the subgraph and there
        are no retries left.
        """
        prefix = ''
        if param_types is not None:
            prefix = 'query '
            prefix += json.dumps(param_types).replace('"', '').replace('{', '(').replace('}', ')')
            prefix += '{'

        querystr = prefix + querystr
        # print(f'Querying The Graph for {querystr}')

        retries_left = QUERY_RETRY_TIMES
        while retries_left > 0:
            try:
                result = self.client.execute(gql(querystr), variable_values=param_values)
            # need to catch Exception here due to stupidity of gql library
            except (requests.exceptions.RequestException, Exception) as e:  # pylint: disable=broad-except  # noqa: E501
                # NB: the lack of a good API error handling by The Graph combined
                # with gql v2 raising bare exceptions doesn't allow us to act
                # better on failed requests. Currently all trigger the retry logic.
                # TODO: upgrade to gql v3 and amend this code on any improvement
                # The Graph does on its API error handling.
                exc_msg = str(e)
                retries_left -= 1
                base_msg = f'The Graph query to {querystr} failed due to {exc_msg}'
                if retries_left:
                    sleep_seconds = RETRY_BACKOFF_FACTOR * pow(2, QUERY_RETRY_TIMES - retries_left)
                    retry_msg = (
                        f'Retrying query after {sleep_seconds} seconds. '
                        f'Retries left: {retries_left}.'
                    )
                    print(f'{base_msg}. {retry_msg}')
                    gevent.sleep(sleep_seconds)
                else:
                    pass
            else:
                break

        print('Got result from The Graph query')
        return result



def get_pairs_from_uniswap():
    """Detect the uniswap v2 pool tokens by using the subgraph"""
    step = 1000
    querystr = """
      pairs(first:$first, skip: $skip, where: {createdAtTimestamp_gt:1609459200}) {
        id
        token0{
          id
          symbol
          name
          decimals
        }
        token1{
          id
          symbol
          name
          decimals
        }
      }
    }
    """
    param_types = {
        '$first': 'Int!', 
        '$skip': 'Int!'
    }
    param_values = {'first': step, 'skip': 0}
    graph = Graph('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')

    contracts = []
    total_pairs_num = 0
    while True:
        print(param_values['skip'])
        # print(f'Querying graph pairs batch {param_values["skip"]} - {param_values["skip"] + step}')
        result = graph.query(querystr, param_types=param_types, param_values=param_values)
        for entry in result['pairs']:
            try:
                contracts.append({
                    'address': entry['id'],
                    'token0': {
                        'address': entry['token0']['id'],
                        'name': entry['token0']['name'],
                        'symbol': entry['token0']['symbol'],
                        'decimals': int(entry['token0']['decimals']),
                    },
                    'token1': {
                        'address': entry['token1']['id'],
                        'name': entry['token1']['name'],
                        'symbol': entry['token1']['symbol'],
                        'decimals': int(entry['token1']['decimals']),
                    },
                })
            except Exception as e:
                print('Error deserializing address while fetching uniswap v2 pool tokens', e)
                sys.exit(1)

            
        pairs_num = len(result['pairs'])
        total_pairs_num += pairs_num
        if pairs_num < step:
            break
        
        # param_values['first'] = total_pairs_num
        param_values['skip'] = total_pairs_num

    return contracts

