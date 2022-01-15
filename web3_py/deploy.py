import json
import os

from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile solidity
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_ADDRESS")))
chain_id = int(os.getenv("CHAIN_ID"))
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# create the contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# deploy contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish...")
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Done! Contract deployed to {txn_receipt.contractAddress}")

# call -> simulate making a call and getting a return value (no state change)
# transact -> make a state change
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# initial value
print(f"Initial storage: {simple_storage.functions.retrieve().call()}")
# store a number
print("Storing a number...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
        "gasPrice": w3.eth.gas_price,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
store_transaction_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_transaction_receipt = w3.eth.wait_for_transaction_receipt(store_transaction_hash)
print("Number stored!")
print(f"Storage after store: {simple_storage.functions.retrieve().call()}")
