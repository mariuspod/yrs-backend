
from decimal import Decimal
from typing import List, Tuple

import pandas as pd
from pony.orm import db_session, select

from db.entities import UserTx


@db_session
def transactions(GOOD_ADDRESSES: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Returns a tuple of DataFrames `(inboundTxs,outboundTxs)`
    '''
    _in = select(
        (
            t.timestamp, 
            t.block, 
            t.hash, 
            t.vault.token.chainid, 
            t.vault.symbol,
            t.vault.token.address, 
            t.type, 
            t.from_address, 
            t.to_address, 
            t.amount, 
            t.price, 
            t.value_usd,
            t.gas_used,
            t.gas_price
        ) for t in UserTx 
            if t.to_address in GOOD_ADDRESSES
            # users can be weird and send things to themselves, we don't care about those
            and t.from_address != t.to_address 
            # if for some reason we have a tx with 0 amount, ignore
            # see `0x05ba797ba30fc4416e1932ac490a89613c525e0b5da4b95b79e9a4e28926e94e`
            and t.amount > 0
        )
    _out = select(
        (
            t.timestamp, 
            t.block, 
            t.hash, 
            t.vault.token.chainid, 
            t.vault.symbol,
            t.vault.token.address, 
            t.type, 
            t.from_address, 
            t.to_address, 
            t.amount, 
            t.price, 
            t.value_usd,
            t.gas_used,
            t.gas_price
        ) for t in UserTx
            if t.from_address in GOOD_ADDRESSES
            # users can be weird and send things to themselves, we don't care about those
            and t.from_address != t.to_address 
            # if for some reason we have a tx with 0 amount, ignore
            # see `0x05ba797ba30fc4416e1932ac490a89613c525e0b5da4b95b79e9a4e28926e94e`
            and t.amount > 0
        )
    
    # create DataFrames
    _in, _out = pd.DataFrame(_in), pd.DataFrame(_out)
    try: _in.columns = ['timestamp','block','hash','chainid','symbol','vault','type','from','to','amount','price','value_usd','gas_used','gas_price']
    except: pass
    try:
        _out.columns = ['timestamp','block','hash','chainid','symbol','vault','type','from','to','amount','price','value_usd','gas_used','gas_price']
        _out = _out.sort_values(['vault','timestamp'],ascending=[True,True]).reset_index(drop=True)
    except: pass
  
    _in.timestamp = pd.to_datetime(_in.timestamp,unit='s')
    _out.timestamp = pd.to_datetime(_out.timestamp,unit='s')
    
    return _in, _out

def unique_tokens_sold(tokens_out: pd.DataFrame) -> List[str]:
    try: return tokens_out['vault'].unique()
    except: return []
    
def tx_list_for_export(_in: pd.DataFrame, _out: pd.DataFrame) -> List[dict]:
    txs = pd.concat([_in,_out]).sort_values(by='timestamp')
    txs['gas_cost'] = txs.gas_price * txs.gas_used / Decimal(1e18)
    txs = txs.drop(columns=['gas_price','gas_used'])
    return [{
        'block': row.block,
        'hash': row.hash,
        'timestamp': row.timestamp,
        'to_address': row.to_address,
        'from_address': row.from_address,
        'amount': row.amount,
        'price': row.price,
        'value_usd': row.value_usd,
    } for row in txs.itertuples()]
    