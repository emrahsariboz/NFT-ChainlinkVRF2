from random import random
from brownie import AdvancedCollectible, accounts, config, convert, interface, network

from scripts.helpful_scripts import get_account
import time
from web3 import Web3
import os


def subscribe_for_VRF():
    account = get_account()
    contract = AdvancedCollectible[-1]
    # Subscribe to the contract
    tx = contract.subscribe({"from": account})
    tx.wait(1)


def fund_with_link():
    print("Funding the subscription...")
    account = get_account()
    contract = AdvancedCollectible[-1]

    # Fund the contract.
    # We need abi of LinkTokenInterface.sol
    link_token_contract = interface.LinkTokenInterface(
        config["networks"][network.show_active()]["link_token"]
    )

    tx = link_token_contract.transferAndCall(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["fee"],
        convert.to_bytes(contract.s_subscriptionId()),
        {"from": account},
    )

    tx.wait(1)


def amount_of_link_available():
    account = get_account()
    contract = AdvancedCollectible[-1]

    vrf_coordinator_contract = interface.VRFCoordinatorV2Interface(
        config["networks"][network.show_active()]["vrf_coordinator"],
    )

    (balance, _, _, _) = vrf_coordinator_contract.getSubscription(
        contract.s_subscriptionId()
    )
    print("Contract balance is ", balance)


def add_user():
    account = get_account()
    contract = AdvancedCollectible[-1]

    print("Adding customer...")

    tx = contract.addUser(contract.address, {"from": account})

    tx.wait(1)


def request_random():
    account = get_account()
    contract = AdvancedCollectible[-1]

    # Request Random
    tx = contract.requestRandom({"from": account})

    print("Waiting for the callback...")

    tx.wait(5)

    while True:
        random_num = contract.randomNum()

        if random_num != 0:
            print("Finally received random num:", random_num)
            break
        else:
            print("Waiting another 5 sn")
            time.sleep(5)


def main():

    account = get_account()

    contract = AdvancedCollectible.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        "0xd89b2bf150e3b9e13446986e571fb9cab24b13cea0a43ea20a6049a85cc807cc",
        {"from": account},
    )

    contract = AdvancedCollectible[-1]

    print(f"The contract deployed at {contract.address}...")

    subscribe_for_VRF()

    # FUND CONTRACT
    fund_with_link()

    # CHECK IF ENOUGH FUND!!

    print("Sub ID...", contract.s_subscriptionId())

    # Add User
    add_user()

    # Request Random
    request_random()

    print(f"The random number is {contract.randomNum()}...")
