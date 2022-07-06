import password
from django.conf import settings
from web3 import Web3


def get_nexid_token_balance():
    w3 = Web3(Web3.HTTPProvider(password.NETWORK_URL))
    nexid_token = w3.eth.contract(address=settings.NEXID_TOKEN_ADDRESS, abi=settings.NEXID_TOKEN_ABI)
    balance = nexid_token.functions.balanceOf(password.ADDRESS).call()
    return w3.fromWei(balance, 'ether')


def get_nexid_nft_balance():
    w3 = Web3(Web3.HTTPProvider(password.NETWORK_URL))
    nexid_nft = w3.eth.contract(address=settings.NEXID_NFT_ADDRESS, abi=settings.NEXID_NFT_ABI)
    return nexid_nft.functions.balanceOf(password.ADDRESS).call()


def get_nexid_nft_price():
    w3 = Web3(Web3.HTTPProvider(password.NETWORK_URL))
    nexid_seller = w3.eth.contract(address=settings.NEXID_SELLER_ADDRESS, abi=settings.NEXID_SELLER_ABI)
    price = nexid_seller.functions.price().call()
    return w3.fromWei(price, 'ether')
