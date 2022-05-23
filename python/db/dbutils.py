from sqlalchemy.orm import Session
from db.database import Pair, Price


def write_price_row(session: Session, row):
    session.add(Price(
        price=row['price'],
        exchange=row['exchange'],
        source=row['source'],
        ts=row['ts'],
        token0='ETH',
        token1='USDT'))
    session.commit()

def write_pair_row(session: Session, row):
    #   token0address = Column(String)
    # token1address = Column(String)
    # pairaddress = Column(String)
    # token0symbol = Column(String)
    # token1symbol = Column(String)
    # created_at = Column(String)
    
    # {"args": {"token0": "0x61F32e4d469Be1C257D6828A128122A64111CA17", "token1": 
    # "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c", 
    # "pair": "0x253925E517DD2F2e67e643263A851eA1CeEf7395", "": 947861}, 
    # "event": "PairCreated", "logIndex": 179, "transactionIndex": 79, 
    # "transactionHash": "0x1b490da8f30dee73b8d1c892a470d3f7c18a13f55bd65cd6e437caeed01b18b3", 
    # "address": "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73", 
    # "blockHash": "0x9d0f7aabe00fcf8810c7983bf4b27efc9446205da013d026762f1ce127a93936", 
    # "blockNumber": 17964820}
    
    session.add(Pair(
        token0address=row['token0address'],
        token1address=row['token1address'],
        pairaddress=row['pairaddress'],
        source=row['source'],
        created_at=row['created_at'],
        token0symbol='ETH',
        exchange=row['exchange'],
        token1symbol='USDT'))
    session.commit()


def get_all_prices(session: Session):
    all_prices = session.query(Price).all()
    # print([f"Price: {i.token0}-{i.token1} | {i.ts} | {i.price}," for i in all_prices])
    return all_prices

def get_all_pairs(session: Session):
    all_prices = session.query(Price).all()
    # print([f"Price: {i.token0}-{i.token1} | {i.ts} | {i.price}," for i in all_prices])
    return all_prices