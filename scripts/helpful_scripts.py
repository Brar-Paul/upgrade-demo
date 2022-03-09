from brownie import (
    accounts,
    network,
    config,
    Contract,
    interface,
)
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "hardhat"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    tx = None
    if proxy_admin_contract:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            tx = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encode_function_call,
                {"from": account},
            )
        else:
            tx = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    else:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            tx = proxy.upgradeToAndCall(
                new_implementation_address, encode_function_call, {"from": account}
            )
        else:
            tx = proxy.upgradeTo(new_implementation_address, {"from": account})
    return tx
