import brownie
import pytest


initial_supply = 100 * pow(10, 18)
amount = 10 * pow(10, 18)

@pytest.fixture(scope="module", autouse=True)
def nexid_token(NexidToken, accounts):
    return accounts[0].deploy(NexidToken, initial_supply)


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.mark.parametrize('name', ["Nexid"])
def test_token_name(nexid_token, name):
    assert nexid_token.name() == name


@pytest.mark.parametrize('symbol', ["NEX"])
def test_token_symbol(nexid_token, symbol):
    assert nexid_token.symbol() == symbol


def test_total_supply(nexid_token):
    assert nexid_token.totalSupply() == initial_supply


def test_tokens_transfer_between_accounts(nexid_token, accounts):
    account0_balance = initial_supply - amount
    nexid_token.transfer(accounts[1], amount, {'from': accounts[0]})
    assert nexid_token.balanceOf(accounts[0]) == account0_balance
    assert nexid_token.balanceOf(accounts[1]) == amount
    nexid_token.transfer(accounts[2], amount, {'from': accounts[1]})
    assert nexid_token.balanceOf(accounts[1]) == 0
    assert nexid_token.balanceOf(accounts[2]) == amount


def test_transfer_exceeds_balance(nexid_token, accounts):
    with brownie.reverts("ERC20: transfer amount exceeds balance"):
        nexid_token.transfer(accounts[0], amount, {'from': accounts[1]})
    assert nexid_token.balanceOf(accounts[0]) == initial_supply
    assert nexid_token.balanceOf(accounts[1]) == 0


def test_approval(nexid_token, accounts):
    account0_balance = initial_supply - amount
    nexid_token.approve(accounts[1], amount, {'from': accounts[0]})
    assert nexid_token.allowance(accounts[0], accounts[1]) == amount
    nexid_token.transferFrom(accounts[0], accounts[1], amount, {'from': accounts[1]})
    assert nexid_token.allowance(accounts[0], accounts[1]) == 0
    assert nexid_token.balanceOf(accounts[0]) == account0_balance
    assert nexid_token.balanceOf(accounts[1]) == amount
