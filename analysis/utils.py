import requests
from bs4 import BeautifulSoup

import pandas as pd


def grab_all():
    #get top 10k addresses with labels
    res = []
    for i in range(1,100+1):
        url = 'https://etherscan.io/accounts/{}?ps=100'.format(i)
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('tbody')
        table_rows = table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            row = [td[2].text.strip(),td[3].text.strip()]
            if row:
                res.append(row)
    df = pd.DataFrame(res, columns=['address', 'label'])
    return df