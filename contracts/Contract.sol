// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";

import "@openzeppelin/contracts/access/Ownable.sol";

contract AdvancedCollectible is VRFConsumerBaseV2, ERC721, Ownable {
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    // An interface used to interact with deployed coordinator contract.
    VRFCoordinatorV2Interface COORDINATOR;

    // Random Number
    uint256 public randomNum;

    // subscription ID.
    uint64 public s_subscriptionId;

    address private _owner;

    uint256 public s_requestId;
    uint16 requestConfirmations = 3;
    uint32 callbackGasLimit = 100000;
    uint32 numWords = 2;

    bytes32 keyHash;
    address vrfCoordinator;
    uint256 public tokenCounter;

    constructor(address _vrfCoordinator, bytes32 _keyHash)
        VRFConsumerBaseV2(_vrfCoordinator)
        ERC721("EMRAH", "EMR")
    {
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
        keyHash = _keyHash;
        tokenCounter = 0;
        _owner = msg.sender;
    }

    function requestRandom() external onlyOwner returns (uint256) {
        s_requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );

        return s_requestId;
    }

    function fulfillRandomWords(
        uint256, /* requestId */
        uint256[] memory randomWords
    ) internal override {
        randomNum = randomWords[0];
        Breed breed = Breed(randomNum % 3);
    }

    function subscribe() external returns (uint64 subId) {
        s_subscriptionId = COORDINATOR.createSubscription();
    }

    function addUser(address _sc) external {
        COORDINATOR.addConsumer(s_subscriptionId, _sc);
    }

    // function createCollectible(string memory tokenURI)
    //     public
    //     returns (bytes32)
    // {
    //     uint256 requestId = requestRandom();
    // }
}
