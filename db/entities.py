from pony.orm import *
from decimal import Decimal
from db.config import connect_db

db = connect_db()

class Address(db.Entity):
    _table_ = "addresses"

    chainid = Required(int)
    address = Required(str)
    PrimaryKey(chainid,address)
    is_contract = Required(bool)
    nickname = Optional(str)

    token = Optional('Token')


class Token(db.Entity):
    _table_ = "tokens"

    token = PrimaryKey(Address, columns=["chainid",'token_address'])
    symbol = Required(str)
    name = Required(str)
    decimals = Required(int)

    user_tx = Set('UserTx', reverse="vault")
    

class UserTx(db.Entity):
    _table_ = "user_txs"

    timestamp = Required(int)
    block = Required(int)
    hash = Required(str)
    log_index = Required(int)
    vault = Required(Token, columns=["chainid","vault"], reverse="user_tx")
    type = Required(str)
    from_address = Required(str, column="from")
    to_address = Required(str, column="to")
    amount = Required(Decimal,38,18)
    price = Required(Decimal,38,18)
    value_usd = Required(Decimal,38,18)
    gas_used = Required(Decimal,38,1)
    gas_price = Required(Decimal,38,1)

    PrimaryKey(hash,log_index)
    

db.generate_mapping(create_tables=False)