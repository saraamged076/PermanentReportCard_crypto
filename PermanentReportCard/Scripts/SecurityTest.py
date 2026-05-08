from web3 import Web3
import json

web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

with open("config.json") as f:
    config = json.load(f)

with open("abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(
    address=config["contract_address"],
    abi=abi
)

# normal user (NOT admin)
user = web3.eth.accounts[1]

try:
    tx = contract.functions.setGrade(
        user, "Hacker", 100
    ).transact({'from': user})

    web3.eth.wait_for_transaction_receipt(tx)

    print(" ERROR: User was able to modify grade!")

except Exception as e:
    print(" PASS: Normal user blocked from admin action")