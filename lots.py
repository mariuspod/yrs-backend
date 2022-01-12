from decimal import Decimal
from typing import List

import numpy as np
import pandas as pd


def delete_active_lot(unspent_lots) -> pd.DataFrame:
    # drop active lot
    unspent_lots = unspent_lots.iloc[1: , :]
    unspent_lots.index = np.arange(len(unspent_lots))
    return unspent_lots

def update_active_lot(unspent_lots, active_lot, sold_amount, sold_gas_used) -> pd.DataFrame:
    unspent_lots.at[0,'amount'] = active_lot.amount - sold_amount
    unspent_lots.at[0,'value_usd'] = active_lot.value_usd - (sold_amount * active_lot.price)
    unspent_lots.at[0,'gas_used'] = active_lot.gas_used - sold_gas_used
    return unspent_lots

def record_spent_lot(unspent_lots, active_lot, sold_amount, sold_gas_used) -> pd.DataFrame:
    if active_lot.amount == sold_amount: return delete_active_lot(unspent_lots)
    else: return update_active_lot(unspent_lots, active_lot, sold_amount, sold_gas_used)

def unspent_lots_for_export(unspent_lots: pd.DataFrame) -> List[dict]:
    unspent_lots['gas_cost'] = unspent_lots.gas_price * unspent_lots.gas_used / Decimal(1e18)
    unspent_lots = unspent_lots.drop(columns=['gas_price','gas_used'])
    return [{
      'test': 0,
    } for row in unspent_lots.itertuples()]
