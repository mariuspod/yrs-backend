from brownie import convert
from flask import request


def method_input():
    choices = ['FIFO','LIFO']
    assert request.json['type'] in choices
    return request.json['type']


def address_inputs():
    sanitized_list = []
    for address in request.json['addresses']:
        address = clean_address(address)
        assert address
        sanitized_list.append(address)
    return sanitized_list


def clean_address(address: str):
    if is_address(address): return convert.to_address(address)
    
    
def is_address(address: str) -> bool:
    return all([
        len(address) == 42
    ])
    

'''curl localhost:5000?type=FIFO&addresses=['0x5b607d28180F7260c6726048E909CB8f1A271CE0','0xe219B069DGGG0c35186Dc97cB550e5Dc3CE863aA7667']'''

'''curl localhost:5000 -H 'Content-Type: application/json' -d '{"type":"FIFO","addresses":["0x5b607d28180F7260c6726048E909CB8f1A271CE0","0xe219B069D0c35186Dc97cB550e5Dc3CE863aA766"]}'  '''