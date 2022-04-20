from brownie import AdvancedCollectible, accounts, config, convert, interface, network
from scripts.helpful_scripts import get_breed
from scripts.metadata.sample_metadata import metadata_template


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))

        metadat_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        print(metadat_file_name)
