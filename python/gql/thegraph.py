import requests
# pretty print is used to print the output in the console in an easy to read format
from pprint import pprint


# function to use requests.post to make an API call to the subgraph url
def run_query():

    # endpoint where you are making the request
    request = requests.post('https://api.thegraph.com/subgraphs/name/aave/protocol'
                            '',
                            json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))


# The Graph query - Query aave for a list of the last 10 flash loans by time stamp
query = """

{
flashLoans (first: 10, orderBy: timestamp, orderDirection: desc,){
  id
  reserve {
    name
    symbol
  }
  amount
  timestamp
}
}
"""
result = run_query(query)

# print the results
print('Print Result - {}'.format(result))
print('#############')
# pretty print the results to make it easier to read
pprint(result)