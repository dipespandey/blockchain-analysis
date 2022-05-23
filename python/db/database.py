from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine

Base = declarative_base()


class Price(Base):
    __tablename__ = "price"
    entry_id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(String)
    exchange = Column(String)
    source = Column(String)
    ts = Column(String)
    token0 = Column(String)
    token1 = Column(String)
    
    def get_ts(self):
        return self.ts

    def __str__(self):
        return f"Price: {self.token0}-{self.token1} | {self.ts} | {self.price}"


class Pair(Base):
    __tablename__ = 'pair'
    entry_id = Column(Integer, primary_key=True, autoincrement=True)
    token0address = Column(String)
    token1address = Column(String)
    pairaddress = Column(String)
    token0symbol = Column(String)
    token1symbol = Column(String)
    created_at = Column(String)
    exchange = Column(String)

    def __str__(self):
        return f"Pair: {self.token0symbol} | {self.token1symbol} | {self.exchange}"


class Token(Base):
    __tablename__ = 'token'
    entry_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String)
    symbol = Column(String)
    decimals = Column(Integer)
    name = Column(String)
    exchange = Column(String)

    def __str__(self):
        return f"Token: {self.symbol} | {self.name} | {self.exchange}"


class Transaction(Base):
    # AttributeDict({
    # 'blockHash': HexBytes('0x55228c776b455a3737f816333edbc535d3470803fdfaca70688707c5f72276ff'), 
    # 'blockNumber': 10008555, 
    # 'from': '0xc9aCf2FEC74eCdA8F3D9F8dd04f7D48Ba305D7c4', 
    # 'gas': 400000, 
    # 'gasPrice': 37081627614, 
    # 'hash': HexBytes('0x105b17f9d75da2de8b6c26c07c03d64ac6172a6eb0bcdef811de320d292d4e60'), 
    # 'input': '0xa7880d4f000000000000000000000000000000000000000000007105d3033aad8674eef8000000000000000000000000b4efd85c19999d84251304bda99e90b92300bd930000000000000000000000003fb2f18065926ddb33e7571475c509541d15da0e000000000000000000000000000000000000000000000002b5e3af16b188000000000000000000000000000000000000000000000000000000000000ee6b2800000000000000000000000000000000000000000000000000df6eb0b2d3ca0000000000000000000000000000000000000000000000000000000000005eb1d901', 
    # 'nonce': 101, 
    # 'r': HexBytes('0x1cc014f540b5c8f8f87607d31ee79a5cbb99f08cfac699c7c42a05dacc07560c'), 
    # 's': HexBytes('0x44c07c208a4607055ea66582fa1a5bc6f7f5b6709777cb59cd6c360f51220a73'), 
    # 'to': '0x70A740fa253FD06840F47d1a3c99B3Fa9ec2d1CB', 
    # 'transactionIndex': 6, 
    # 'type': '0x0', 
    # 'v': 37, 
    # 'value': 0})
    __tablename__ = 'transaction'
    entry_id = Column(Integer, primary_key=True, autoincrement=True)
    blockchain = Column(String)
    blockNumber = Column(Integer)
    from_ = Column(String)
    to_ = Column(String)
    gas = Column(Integer)
    gasPrice = Column(Integer)
    hash = Column(String)
    value = Column(String)

    def __str__(self):
        return f"Transaction: {self.blockchain} | {self.from_} | {self.to_}"



def make_tables():
    url = "postgresql+psycopg2://postgres:mypassword@localhost:5432/postgres"
    # Create database if it does not exist.
    engine = create_engine(url, echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    
    print(engine)
    try:
        Token.__table__.create(engine)
    except Exception as e:
        print(e)
        print('Token table already exists..')
    try:
        Price.__table__.create(engine)
    except Exception as e:
        print(e)
        print('Price table already exists..')
    try:
        Pair.__table__.create(engine)
    except Exception as e:
        print('Pair table already exists..')
    try:
        Transaction.__table__.create(engine)
    except Exception as e:
        print(e)
        print('Transaction table already exists..')


def create_connection():
    """Main entry point of program"""
    # Connect to the database using SQLAlchemy
    url = "postgresql+psycopg2://postgres:mypassword@localhost:5432/postgres"
    # Create database if it does not exist.
    engine = create_engine(url, echo=True)
    print(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    return session