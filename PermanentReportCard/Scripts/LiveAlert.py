from web3 import Web3
import json
import time

# connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

print("Connected:", web3.is_connected())

# load contract address
with open("config.json") as f:
    config = json.load(f)

contract_address = config["contract_address"]

# load ABI
with open("abi.json") as f:
    abi = json.load(f)

# connect to contract 
contract = web3.eth.contract(address=contract_address, abi=abi)

# start listening
last_block = web3.eth.block_number

print("Listening for grade changes...")

while True:
    current_block = web3.eth.block_number

    if current_block > last_block:
        for i in range(last_block + 1, current_block + 1):
            block = web3.eth.get_block(i, full_transactions=True)

            for tx in block.transactions:
                # check if transaction is to our contract
                if tx['to'] == contract.address:
                    print("🚨 ALERT: A grade change just happened!")

        last_block = current_block

    time.sleep(2)