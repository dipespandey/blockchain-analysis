from sqlalchemy.orm import Session
from db.database import Pair, Price


def write_price_row(session: Session, row):
    session.add(Price(price=row['price'],
                      source=row['source'],
                      ts=row['ts'],
                      token0='ETH',
                      token1='USDT'))
    session.commit()

def write_pair_row(session: Session, row):
    session.add(Pair(price=row['price'],
                      source=row['source'],
                      ts=row['ts'],
                      token0='ETH',
                      token1='USDT'))
    session.commit()


def get_all_prices(session: Session):
    all_prices = session.query(Price).all()
    print([f"Price: {i.token0}-{i.token1} | {i.ts} | {i.price}," for i in all_prices])
    return all_prices

def get_all_pairs(session: Session):
    all_prices = session.query(Price).all()
    print([f"Price: {i.token0}-{i.token1} | {i.ts} | {i.price}," for i in all_prices])
    return all_prices