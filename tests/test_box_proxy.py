from scripts.helpful_scripts import encode_function_data, get_account
from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_proxy_delegates_calls():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 10000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retreive() == 0
    proxy_box.store(1, {"from": account})
    assert proxy_box.retreive() == 1
