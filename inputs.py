from brownie import convert
from flask import request


def method_input():
    choices = ['FIFO','LIFO']
    assert request.json['type'] in choices
    return request.json['type']


def address_inputs():
    good_list, bad_list = [], []
    for address in request.json['addresses']:
        clean = clean_address(address)
        if clean: good_list.append(clean)
        else: bad_list.append(address)
    return good_list, bad_list


def clean_address(address: str):
    if is_address(address): return convert.to_address(address)
    
    
def is_address(address: str) -> bool:
    return all([
        len(address) == 42
    ])
    
