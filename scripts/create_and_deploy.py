from random import random
from brownie import AdvancedCollectible, accounts, config, convert, interface, network
from scripts.helpful_scripts import get_account
import time
from web3 import Web3


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
        Web3.toWei(2, "ether"),  # 2 LINK
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


def main():

    account = get_account()

    contract = AdvancedCollectible.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["keyHash"],
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
