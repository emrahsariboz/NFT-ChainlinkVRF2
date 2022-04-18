from brownie import (
    AdvancedCollectible,
    accounts,
    config,
    convert,
    interface,
)

from scripts.helpful_scripts import get_account


import time
from web3 import Web3


def main():
    link_token_address = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"

    account = get_account()

    contract = AdvancedCollectible.deploy(
        "0x6168499c0cFfCaCD319c818142124B7A15E857ab",
        "0xd89b2bf150e3b9e13446986e571fb9cab24b13cea0a43ea20a6049a85cc807cc",
        {"from": account},
    )

    contract = AdvancedCollectible[-1]

    print(f"The contract deployed at {contract.address}")

    # Subscribe to the contract
    tx = contract.subscribe({"from": account})
    tx.wait(1)

    # Fund the contract.
    # We need abi of LinkTokenInterface.sol

    link_token_contract = interface.LinkTokenInterface(link_token_address)

    tx = link_token_contract.transferAndCall(
        "0x6168499c0cFfCaCD319c818142124B7A15E857ab",
        50000000000000000,
        convert.to_bytes(contract.s_subscriptionId()),
        {"from": account},
    )

    tx.wait(1)

    print("Sub ID", contract.s_subscriptionId())

    # Add owner
    tx = contract.addUser({"from": account})

    tx.wait(1)

    # Request Random
    tx = contract.requestRandom({"from": account})

    print("Waiting for the callback...")

    time.sleep(60)

    print(f"The random number is {contract.s_randomWords[0]}")
