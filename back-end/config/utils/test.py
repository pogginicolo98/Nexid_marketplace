from pprint import pprint
import json
from web3 import Web3
from pathlib import Path
from nfts_redis import record_nfts_on_redis, get_nfts_from_redis

NETWORK_URL = 'HTTP://127.0.0.1:8545'
ADDRESS = '0xf920a836d84ceA0d1E50EcECe3EdbF7Fc4DBe16e'
PRIVATE_KEY = 'a7461cb566120e3cda394a1d2c32e2624567886edccacb2f3872cc0119399c04'

SC_DIR = Path(__file__).resolve().parent.parent / 'smart-contracts'

NEXID_TOKEN_ADDRESS = '0x3Fd99F3E669F9143935B92f5597f2FbE19E4376F'
with open(SC_DIR / 'NexidToken.json', 'r') as f:
    NEXID_TOKEN_ABI = json.load(f)['abi']

NEXID_NFT_ADDRESS = '0x2167f3E23A5527F85B1b19211c3c35BC40af14DA'
with open(SC_DIR / 'NexidNFT.json', 'r') as f:
    NEXID_NFT_ABI = json.load(f)['abi']

NEXID_SELLER_ADDRESS = '0xae9f526D1043bf6cD394f795c3F57c04c7318324'
with open(SC_DIR / 'NexidSeller.json', 'r') as f:
    NEXID_SELLER_ABI = json.load(f)['abi']

w3 = Web3(Web3.HTTPProvider(NETWORK_URL))
w3.eth.default_account = ADDRESS
nexid_token = w3.eth.contract(address=NEXID_TOKEN_ADDRESS, abi=NEXID_TOKEN_ABI)
nexid_nft = w3.eth.contract(address=NEXID_NFT_ADDRESS, abi=NEXID_NFT_ABI)
nexid_seller = w3.eth.contract(address=NEXID_SELLER_ADDRESS, abi=NEXID_SELLER_ABI)


def purchase(token_id):
    price = nexid_seller.functions.price().call()
    tx_hash = nexid_token.functions.approve(NEXID_SELLER_ADDRESS, price).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    tx_hash = nexid_seller.functions.purchase(token_id).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    pprint(receipt)
    print(type(receipt))


def get_nfts_for_sale():
    balance = nexid_nft.functions.balanceOf(NEXID_SELLER_ADDRESS).call()
    if balance > 0:
        nfts = []
        for i in range(balance):
            token_id = nexid_nft.functions.tokenOfOwnerByIndex(NEXID_SELLER_ADDRESS, i).call()
            token_uri = nexid_nft.functions.tokenURI(token_id).call()
            nfts.append(json.dumps({
                'token_id': token_id,
                'token_uri': token_uri
            }))
        record_nfts_on_redis(nfts)
    else:
        return None


# nfts = get_nfts_for_sale()
# if nfts is not None:
#     record_nfts_on_redis(nfts)
# values = get_nfts_from_redis()
# if values is not None:
#     redis_nfts = []
#     for value in values:
#         redis_nfts.append(json.loads(value))
#     pprint(redis_nfts)
# else:
#     print("No nft recorded on redis")

purchase(2)