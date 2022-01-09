import pandas as pd

from flask import Flask
from pony.orm import db_session, select
from inputs import address_inputs, method_input
from entities import UserTx

app = Flask(__name__)
          

@app.route("/", methods=['POST'])
def hello_yrs_backend():
    with db_session:
      # user input goes here
      # TODO: figure out how to get user input from vue into this
      ADDRESSES, METHOD = address_inputs(), method_input()
      
      # query txs
      result = select(
        (
          t.timestamp, 
          t.block, 
          t.hash, 
          t.log_index, 
          t.vault.token.chainid, 
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
          if t.from_address in ADDRESSES or t.to_address in ADDRESSES
          # users can be weird and send things to themselves, we don't care about those
          and t.from_address != t.to_address 
      )

      # convert to dataframe
      result = pd.DataFrame(result)
      # rename columns
      result.columns = ['timestamp','block','hash','log_index','chainid','vault','type','from','to','amount','price','value_usd','gas_used','gas_price']
      # convert to json
      result = result.to_json()
      # voila
      return result

