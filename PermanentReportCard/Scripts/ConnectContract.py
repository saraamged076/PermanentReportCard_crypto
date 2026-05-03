from web3 import Web3
import json

# connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

print("Connected:", web3.is_connected())

# contract address 
with open("config.json") as f:
    config = json.load(f)

contract_address = config["contract_address"]

# ABI 
with open("abi.json") as f:
    abi = json.load(f)

# connect to contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# test getGrade
address = "0x486416D9A11A47Ab1C745586bB0623259c905c5a"

name, grade = contract.functions.getGrade(address).call()

print("Name:", name)
print("Grade:", grade)