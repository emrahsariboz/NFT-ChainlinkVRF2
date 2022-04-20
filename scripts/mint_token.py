from random import random
from brownie import AdvancedCollectible, accounts, config, convert, interface, network
from hypothesis import event

from scripts.helpful_scripts import get_account
import time
from web3 import Web3
import os

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def main():
    account = get_account()
    contract = AdvancedCollectible[-1]

    tx = contract.createCollectible(sample_token_uri, {"from": account})

    print("Collectible Created!!!")

    tx.wait(5)

    print("Waiting for the callback!")
    time.sleep(20)

    while True:
        random_num = contract.randomNum()
        if random_num != 0:
            print("Finally received random num:", random_num)
            break
        else:
            print("Waiting another 5 sn")
            time.sleep(5)
    print(tx.events)
    print(tx.events["requestConfirmationEvent"])


# def request_random():
#     account = get_account()
#     contract = AdvancedCollectible[-1]

#     # Request Random
#     tx = contract.createCollectible({"from": account})

#     print("Waiting for the callback...")

#     tx.wait(5)

#     while True:
#         random_num = contract.randomNum()
#         if random_num != 0:
#             print("Finally received random num:", random_num)
#             break
#         else:
#             print("Waiting another 5 sn")
#             time.sleep(5)
