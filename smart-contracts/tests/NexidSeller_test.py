import brownie
import pytest


initial_supply = 100 * pow(10, 18)
price = 10 * pow(10, 18)


@pytest.fixture(scope="module", autouse=True)
def nexid_token(NexidToken, accounts):
    return accounts[0].deploy(NexidToken, initial_supply)


@pytest.fixture(scope="module", autouse=True)
def nexid_nft(NexidNFT, accounts):
    return accounts[0].deploy(NexidNFT)


@pytest.fixture(scope="module", autouse=True)
def nexid_seller(NexidSeller, nexid_token, nexid_nft, accounts):
    return accounts[0].deploy(NexidSeller, nexid_token.address, nexid_nft.address, price)


@pytest.fixture(scope="function", autouse=True)
def setup_nexid_seller(nexid_token, nexid_nft, nexid_seller, accounts):
    nexid_nft.mint("token uri", {'from': accounts[0]})
    token_id = nexid_nft.tokenOfOwnerByIndex(accounts[0], 0)
    nexid_nft.transferFrom(accounts[0], nexid_seller.address, token_id, {'from': accounts[0]})
    nexid_token.transfer(accounts[1], price, {'from': accounts[0]})
    return token_id


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_purchase(nexid_token, nexid_nft, nexid_seller, setup_nexid_seller, accounts):
    token_id = setup_nexid_seller
    nexid_token.approve(nexid_seller.address, price, {'from': accounts[1]})
    nexid_seller.purchase(token_id, {'from': accounts[1]})
    assert nexid_token.balanceOf(accounts[1]) == 0
    assert nexid_token.balanceOf(nexid_seller.address) == price
    assert nexid_nft.ownerOf(token_id) == accounts[1]


def test_purchase_without_approval(nexid_token, nexid_nft, nexid_seller, setup_nexid_seller, accounts):
    token_id = setup_nexid_seller
    with brownie.reverts("NexidToken not approved."):
        nexid_seller.purchase(token_id, {'from': accounts[1]})
    assert nexid_token.balanceOf(accounts[1]) == price
    assert nexid_token.balanceOf(nexid_seller.address) == 0
    assert nexid_nft.ownerOf(token_id) == nexid_seller.address


def test_purchase_invalid_token_id(nexid_token, nexid_nft, nexid_seller, accounts):
    nexid_nft.mint("token uri 2", {'from': accounts[0]})
    token_id = nexid_nft.tokenOfOwnerByIndex(accounts[0], 0)
    nexid_token.approve(nexid_seller.address, price, {'from': accounts[1]})
    with brownie.reverts("NFT not for sale."):
        nexid_seller.purchase(token_id, {'from': accounts[1]})
    assert nexid_token.balanceOf(accounts[1]) == price
    assert nexid_token.balanceOf(nexid_seller.address) == 0
    assert nexid_nft.ownerOf(token_id) == accounts[0]


def test_purchase_insufficient_balance(nexid_token, nexid_nft, nexid_seller, setup_nexid_seller, accounts):
    token_id = setup_nexid_seller
    nexid_token.approve(nexid_seller.address, price, {'from': accounts[2]})
    with brownie.reverts("Not enough Nexid tokens."):
        nexid_seller.purchase(token_id, {'from': accounts[2]})
    assert nexid_token.balanceOf(accounts[2]) == 0
    assert nexid_token.balanceOf(nexid_seller.address) == 0
    assert nexid_nft.ownerOf(token_id) == nexid_seller.address


def test_withdraw_by_owner(nexid_token, nexid_nft, nexid_seller, setup_nexid_seller, accounts):
    token_id = setup_nexid_seller
    amount = price / 2
    nexid_token.approve(nexid_seller.address, price, {'from': accounts[1]})
    nexid_seller.purchase(token_id, {'from': accounts[1]})
    nexid_seller.withdraw(amount, {'from': accounts[0]})
    assert nexid_token.balanceOf(nexid_seller.address) == price - amount
    assert nexid_token.balanceOf(accounts[0]) == initial_supply - price + amount


def test_withdraw_exceed_balance(nexid_token, nexid_nft, nexid_seller, setup_nexid_seller, accounts):
    token_id = setup_nexid_seller
    amount = price * 2
    nexid_token.approve(nexid_seller.address, price, {'from': accounts[1]})
    nexid_seller.purchase(token_id, {'from': accounts[1]})
    with brownie.reverts("The amount exceeds the available balance."):
        nexid_seller.withdraw(amount, {'from': accounts[0]})
    assert nexid_token.balanceOf(nexid_seller.address) == price
    assert nexid_token.balanceOf(accounts[0]) == initial_supply - price


def test_withdraw_by_user(nexid_token, nexid_nft, nexid_seller, setup_nexid_seller, accounts):
    token_id = setup_nexid_seller
    amount = price / 2
    nexid_token.approve(nexid_seller.address, price, {'from': accounts[1]})
    nexid_seller.purchase(token_id, {'from': accounts[1]})
    with brownie.reverts("Only owner can call this function."):
        nexid_seller.withdraw(amount, {'from': accounts[1]})
    assert nexid_token.balanceOf(nexid_seller.address) == price
    assert nexid_token.balanceOf(accounts[1]) == 0
