from brownie import MyToken
from web3 import Web3

from .helpful_scripts import get_account

initial_supply = Web3.toWei(1000, "ether")


def main():
    account = get_account()
    my_token = MyToken.deploy(initial_supply, {"from": account})
    print(my_token.name())
