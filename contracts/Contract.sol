// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";

contract AdvancedCollectible is VRFConsumerBaseV2, ERC721 {
    // An interface used to create subscription, etc.
    VRFCoordinatorV2Interface COORDINATOR;

    uint256[] public s_randomWords;
    uint256 public randomNum;
    address public owner;

    uint64 public s_subscriptionId;
    uint256 public s_requestId;
    uint16 requestConfirmations = 3;
    uint32 callbackGasLimit = 100000;
    uint32 numWords = 2;

    bytes32 keyHash;
    address vrfCoordinator;
    uint256 public tokenCounter;

    event ReceivedCallback(uint256);

    constructor(address _vrfCoordinator, bytes32 _keyHash)
        VRFConsumerBaseV2(_vrfCoordinator)
        ERC721("EMRAH", "EMR")
    {
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
        keyHash = _keyHash;
        tokenCounter = 0;
        owner = msg.sender;
    }

    function requestRandom() external {
        s_requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
    }

    function fulfillRandomWords(
        uint256, /* requestId */
        uint256[] memory randomWords
    ) internal override {
        s_randomWords = randomWords;
        randomNum = s_randomWords[0];
    }

    function subscribe() external returns (uint64 subId) {
        s_subscriptionId = COORDINATOR.createSubscription();
    }

    function addUser(address _sc) external {
        COORDINATOR.addConsumer(s_subscriptionId, _sc);
    }
}
