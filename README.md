NFT mint functionality, where `_mint` operation uses Verifiable Random Function (VRF) from Chainlink. Note that this application use Vertion2. 


## How does Chainlink VRF Version2 work?

- Deploy your smart contract
- Create subscription 
- Fund your subscription. In the example, I funded with 2 LINK. 
- Add a consumer of your subscription, which is the address of the contract you deployed.
- Request randomness, wait for the fallback call. 


## How to run?

This version is configured to run on Rinkeby test net. Assuming you have `.env` file with the private key of your account:

`brownie run scripts/create_and_deploy.py --network rinkeby`
