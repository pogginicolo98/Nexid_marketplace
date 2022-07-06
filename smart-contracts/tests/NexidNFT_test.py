import brownie
import pytest


@pytest.fixture(scope="module", autouse=True)
def nexid_nft(NexidNFT, accounts):
    return accounts[0].deploy(NexidNFT)


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.mark.parametrize('name', ["Nexid NFT"])
def test_token_name(nexid_nft, name):
    assert nexid_nft.name() == name


@pytest.mark.parametrize('symbol', ["ID"])
def test_token_symbol(nexid_nft, symbol):
    assert nexid_nft.symbol() == symbol


def test_owner(nexid_nft, accounts):
    assert nexid_nft.owner() == accounts[0]


def test_minting(nexid_nft, accounts):
    nexid_nft.mint("token uri", {'from': accounts[0]})
    assert nexid_nft.balanceOf(accounts[0]) == 1


def test_token_transfer_between_accounts(nexid_nft, accounts):
    nexid_nft.mint("token uri", {'from': accounts[0]})
    token_id = nexid_nft.tokenOfOwnerByIndex(accounts[0], 0)
    nexid_nft.transferFrom(accounts[0], accounts[1], token_id)
    assert nexid_nft.balanceOf(accounts[0]) == 0
    assert nexid_nft.balanceOf(accounts[1]) == 1


def test_transfer_without_permission(nexid_nft, accounts):
    nexid_nft.mint("token uri", {'from': accounts[0]})
    token_id = nexid_nft.tokenOfOwnerByIndex(accounts[0], 0)
    with brownie.reverts("ERC721: transfer caller is not owner nor approved"):
        nexid_nft.transferFrom(accounts[0], accounts[1], token_id, {'from': accounts[2]})
    assert nexid_nft.ownerOf(token_id) == accounts[0]


def test_approval(nexid_nft, accounts):
    nexid_nft.mint("token uri", {'from': accounts[0]})
    token_id = nexid_nft.tokenOfOwnerByIndex(accounts[0], 0)
    nexid_nft.approve(accounts[1], token_id, {'from': accounts[0]})
    assert nexid_nft.getApproved(token_id) == accounts[1]
    nexid_nft.transferFrom(accounts[0], accounts[1], token_id, {'from': accounts[1]})
    assert nexid_nft.ownerOf(token_id) == accounts[1]


def test_approval_for_all(nexid_nft, accounts):
    nexid_nft.mint("token uri", {'from': accounts[0]})
    nexid_nft.mint("token uri", {'from': accounts[0]})
    token_id = nexid_nft.tokenOfOwnerByIndex(accounts[0], 1)
    nexid_nft.setApprovalForAll(accounts[1], True, {'from': accounts[0]})
    assert nexid_nft.isApprovedForAll(accounts[0], accounts[1]) == True
    nexid_nft.transferFrom(accounts[0], accounts[1], token_id, {'from': accounts[1]})
    assert nexid_nft.ownerOf(token_id) == accounts[1]
