// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract AdvancedCollectible is VRFConsumerBaseV2, ERC721URIStorage, Ownable {
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
    uint32 callbackGasLimit = 2000000;
    uint32 numWords = 2;

    bytes32 keyHash;
    address vrfCoordinator;
    uint256 public tokenCounter;

    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(uint256 => address) public requestIdToSender;
    mapping(uint256 => string) public requestIdToURI;
    mapping(uint256 => uint256) public requestIdToTokenId;

    event requestConfirmationEvent(address sender, string URI, uint256 id);

    constructor(address _vrfCoordinator, bytes32 _keyHash)
        VRFConsumerBaseV2(_vrfCoordinator)
        ERC721("AAA", "A01")
    {
        COORDINATOR = VRFCoordinatorV2Interface(_vrfCoordinator);
        keyHash = _keyHash;
        tokenCounter = 0;
        _owner = msg.sender;
    }

    function createCollectible(string memory tokenURI) public {
        requestRandom(tokenURI);
        // requestIdToSender[s_requestId] = msg.sender;
        // requestIdToURI[s_requestId] = tokenURI;
        // emit requestConfirmationEvent(msg.sender, tokenURI, s_requestId);
    }

    function requestRandom(string memory tokenURI) internal {
        s_requestId = COORDINATOR.requestRandomWords(
            keyHash,
            s_subscriptionId,
            requestConfirmations,
            callbackGasLimit,
            numWords
        );
        requestIdToSender[s_requestId] = msg.sender;
        requestIdToURI[s_requestId] = tokenURI;
        emit requestConfirmationEvent(msg.sender, tokenURI, s_requestId);
    }

    function fulfillRandomWords(
        uint256, /* requestId */
        uint256[] memory randomWords
    ) internal override {
        randomNum = randomWords[0];

        Breed breed = Breed(randomNum % 3);
        uint256 newItemId = tokenCounter;

        tokenIdToBreed[newItemId] = breed;

        address dogOwner = requestIdToSender[s_requestId];
        string memory tokenURI = requestIdToURI[s_requestId];

        _safeMint(dogOwner, newItemId);

        tokenCounter += 1;
    }

    // These can be applied in the scripts??
    // Can we use interface??
    function subscribe() external returns (uint64 subId) {
        s_subscriptionId = COORDINATOR.createSubscription();
    }

    function addUser(address _sc) external {
        COORDINATOR.addConsumer(s_subscriptionId, _sc);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // pug, shiba inu, st bernard
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner or not approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
