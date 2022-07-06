from brownie import NexidToken, NexidNFT, NexidSeller, accounts


def deploy_nexid_token(sender):
    initial_supply = 1000 * pow(10, 18)
    return NexidToken.deploy(initial_supply, {'from': sender})


def deploy_nexid_nft(sender):
    return NexidNFT.deploy({'from': sender})


def deploy_nexid_seller(nexid_token_address, nexid_nft_address, sender):
    price = 10 * pow(10, 18)
    return NexidSeller.deploy(nexid_token_address, nexid_nft_address, price, {'from': sender})


def distribute_nexid_tokens(nexid_token, sender, receiver1, receiver2, receiver3):
    total_supply = nexid_token.balanceOf(sender)
    amount = total_supply / 4
    nexid_token.transfer(receiver1, amount, {'from': sender})
    nexid_token.transfer(receiver2, amount, {'from': sender})
    nexid_token.transfer(receiver3, amount, {'from': sender})


def setup_nexid_seller(nexid_nft, nexid_seller, sender):
    for i in range(9):
        nexid_nft.mint(f'Token uri {i}', {'from': sender})
        token_id = nexid_nft.tokenOfOwnerByIndex(sender, 0)
        nexid_nft.transferFrom(sender, nexid_seller.address, token_id, {'from': sender})


def purchase_from_nexid_seller(nexid_token, nexid_nft, nexid_seller, sender):
    price = nexid_seller.price()
    token_id = nexid_nft.tokenOfOwnerByIndex(nexid_seller.address, 0)
    nexid_token.approve(nexid_seller.address, price, {'from': sender})
    nexid_seller.purchase(token_id, {'from': sender})


def withdraw_from_nexid_seller(nexid_seller, sender):
    amount = nexid_seller.price()
    nexid_seller.withdraw(amount, {'from': sender})


def main():
    owner = accounts.load('ganache-gui-0')
    acc1 = accounts.load('ganache-gui-1')
    acc2 = accounts.load('ganache-gui-2')
    django = accounts.load('ganache-gui-django')

    nexid_token = deploy_nexid_token(owner)
    nexid_nft = deploy_nexid_nft(owner)
    nexid_seller = deploy_nexid_seller(nexid_token.address, nexid_nft.address, owner)

    distribute_nexid_tokens(nexid_token, owner, acc1, acc2, django)
    setup_nexid_seller(nexid_nft, nexid_seller, owner)
    purchase_from_nexid_seller(nexid_token, nexid_nft, nexid_seller, acc1)
    purchase_from_nexid_seller(nexid_token, nexid_nft, nexid_seller, acc2)
    withdraw_from_nexid_seller(nexid_seller, owner)
