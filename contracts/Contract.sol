// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";

//import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";

// Chainlink V2 --> Subscription ID is 2882!

// interface Ichainlink {
//     function transferAndCall(
//         address to,
//         uint256 value,
//         bytes calldata data
//     ) external returns (bool success);
// }

contract AdvancedCollectible is VRFConsumerBaseV2, ERC721 {
    // An interface used to create subscription, etc.
    VRFCoordinatorV2Interface COORDINATOR;

    uint256[] public s_randomWords;
    address public owner;

    uint64 public s_subscriptionId;
    uint256 public s_requestId;
    uint16 requestConfirmations = 3;
    uint32 callbackGasLimit = 100000;
    uint32 numWords = 1;

    //address vrfCoordinator = 0x6168499c0cFfCaCD319c818142124B7A15E857ab;
    //bytes32 keyHash =0xd89b2bf150e3b9e13446986e571fb9cab24b13cea0a43ea20a6049a85cc807cc;
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
    }

    function subscribe() external returns (uint64 subId) {
        s_subscriptionId = COORDINATOR.createSubscription();
    }

    function addUser() external {
        COORDINATOR.addConsumer(s_subscriptionId, owner);
    }

    // function fundSubscription(
    //     address _linkAddress,
    //     address _to,
    //     uint256 _value,
    //     bytes calldata _data
    // ) external {
    //     Ichainlink(_linkAddress).transferAndCall(
    //         _to,
    //         _value,
    //         abi.encode(_data)
    //     );
    // }
}
