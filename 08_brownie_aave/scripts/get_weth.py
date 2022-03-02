from brownie import interface, config, network

from .helpful_scripts import get_account


def main():
    get_weth()


def get_weth():
    account = get_account()

    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    transaction = weth.deposit({"from": account, "value": 0.1 * 10**18})
    transaction.wait(1)
    print("Received 0.1 WETH")
    return transaction
