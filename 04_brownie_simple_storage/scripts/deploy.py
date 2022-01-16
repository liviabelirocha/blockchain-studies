from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    account = get_account()
    print("Deploying Contract...")
    simple_storage = SimpleStorage.deploy({"from": account})
    print(f"Done! Contract deployed to {simple_storage}")

    # initial value
    stored_value = simple_storage.retrieve()
    print(f"Initial storage: {stored_value}")
    # store a number
    print("Storing a number...")
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_store_value = simple_storage.retrieve()
    print("Number stored!")
    print(f"Storage after store: {updated_store_value}")


def get_account():
    return (
        accounts[0]
        if network.show_active() == "development"
        else accounts.add(config["wallets"]["from_key"])
    )


def main():
    deploy_simple_storage()
