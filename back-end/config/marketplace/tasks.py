import json
import password
from celery import shared_task
from config.celery import app
from django.conf import settings
from redis import Redis
from utils.nfts_redis import record_nfts_on_redis, record_status_purchase
from web3 import Web3


@shared_task(name="update_nfts_for_sale")
def update_nfts_for_sale():
    w3 = Web3(Web3.HTTPProvider(password.NETWORK_URL))
    w3.eth.default_account = password.ADDRESS
    nexid_nft = w3.eth.contract(address=settings.NEXID_NFT_ADDRESS, abi=settings.NEXID_NFT_ABI)

    balance = nexid_nft.functions.balanceOf(settings.NEXID_SELLER_ADDRESS).call()
    if balance > 0:
        nfts = []
        for i in range(balance):
            token_id = nexid_nft.functions.tokenOfOwnerByIndex(settings.NEXID_SELLER_ADDRESS, i).call()
            token_uri = nexid_nft.functions.tokenURI(token_id).call()
            nfts.append(json.dumps({
                'token_id': token_id,
                'token_uri': token_uri
            }))
        record_nfts_on_redis(nfts)


@app.task()
def check_transaction(token_id, tx_hash):
    w3 = Web3(Web3.HTTPProvider(password.NETWORK_URL))
    if w3.eth.get_transaction(tx_hash) is not None:
        redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
        if redis_client.exists(token_id):
            if redis_client.get(token_id) == 'Approving':
                status = 'Approved'
                record_status_purchase(token_id, status)
            else:
                status = 'Purchased'
                record_status_purchase(token_id, status)
    check_transaction.apply_async((token_id, tx_hash,), countdown=10, expires=30)


@app.task()
def purchase_nft(token_id):
    w3 = Web3(Web3.HTTPProvider(password.NETWORK_URL))
    w3.eth.default_account = password.ADDRESS
    nexid_token = w3.eth.contract(address=settings.NEXID_TOKEN_ADDRESS, abi=settings.NEXID_TOKEN_ABI)
    nexid_seller = w3.eth.contract(address=settings.NEXID_SELLER_ADDRESS, abi=settings.NEXID_SELLER_ABI)

    status = "Pending"
    price = nexid_seller.functions.price().call()
    allowance = nexid_token.functions.allowance(w3.eth.default_account, settings.NEXID_SELLER_ADDRESS).call()
    if allowance < price:
        status = "Approving"
        max_amount = w3.toWei(2**64-1, 'ether')
        tx_hash_approve = nexid_token.functions.approve(settings.NEXID_SELLER_ADDRESS, max_amount).transact()
        check_transaction.apply_async((token_id, tx_hash_approve,), countdown=10, expires=30)
    record_status_purchase(token_id, status)
    tx_hash_purchase = nexid_seller.functions.purchase(token_id).transact()
    check_transaction.apply_async((token_id, tx_hash_purchase,), countdown=10, expires=30)

