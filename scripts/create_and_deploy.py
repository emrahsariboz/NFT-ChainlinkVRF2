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
import os


def main():
    link_token_address = "0x01BE23585060835E02B77ef475b0Cc51aA1e0709"
    vrf_coordinator = "0x6168499c0cFfCaCD319c818142124B7A15E857ab"
    keyHash = "0xd89b2bf150e3b9e13446986e571fb9cab24b13cea0a43ea20a6049a85cc807cc"
    account = get_account()

    contract = AdvancedCollectible.deploy(
        vrf_coordinator,
        keyHash,
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
        vrf_coordinator,
        2000000000000000000,
        convert.to_bytes(contract.s_subscriptionId()),
        {"from": account},
    )

    tx.wait(1)

    # CHECK IF ENOUGH FUND!!
    vrf_coordinator_contract = interface.VRFCoordinatorV2Interface(vrf_coordinator)

    (balance, _, _, _) = vrf_coordinator_contract.getSubscription(
        contract.s_subscriptionId()
    )

    print("Contract balance is ", balance)
    print("x" * 50)
    print("Sub ID", contract.s_subscriptionId())

    tx = contract.addUser(contract.address, {"from": account})

    tx.wait(1)

    # Request Random
    tx = contract.requestRandom({"from": account})

    print("Waiting for the callback...")

    time.sleep(70)

    print(f"The random number is {contract.randomNum()}")
