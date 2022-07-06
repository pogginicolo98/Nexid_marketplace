from brownie import NexidToken, accounts


def deploy_nexid_token(sender):
    initial_supply = 100 * pow(10, 18)
    return NexidToken.deploy(initial_supply, {'from': sender})


def main():
    nexid_token = deploy_nexid_token(accounts[0])
    print("**************************************************")
    balance = nexid_token.balanceOf(accounts[0])
    print(balance)
    print(type(balance))
    print("**************************************************")
