from distutils.command.config import config
from brownie import (
    accounts,
    network,
    config,
    Contract,
)

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-gui-2"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    current_network = network.show_active()
    if (
        current_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or current_network in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    # Not local network. Retreieve private_key.
    return accounts.add(config["wallets"]["from_key"])


contract_reference = {}


def get_contract_address(contract_name):
    contract_type = contract_reference[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pass
    else:
        contract_address = config["networks"][network.show_active()][contract_name]

        contract = Contract.from_abi(
            contract_type._name,
            contract_address,
            contract_type.abi,
        )

    return contract
