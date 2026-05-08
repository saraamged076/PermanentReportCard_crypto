from web3 import Web3
import json
import csv

# connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

print("Connected:", web3.is_connected())

# load config
with open("config.json") as f:
    config = json.load(f)

contract_address = Web3.to_checksum_address(config["contract_address"])

# load ABI
with open("abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(address=contract_address, abi=abi)

# ================== COLLECT DATA ==================

accounts = web3.eth.accounts

snapshot = []

for acc in accounts:
    acc = Web3.to_checksum_address(acc)

    # coin balance
    coin = contract.functions.getBalance(acc).call()

    # ETH balance
    eth = web3.eth.get_balance(acc)
    eth = web3.from_wei(eth, 'ether')

    snapshot.append([acc, coin, float(eth)])

# ================== SAVE CSV ==================

filename = "balance_snapshot.csv"

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    # header
    writer.writerow(["Account Address", "Grade Coin Balance", "ETH Balance"])

    # data
    writer.writerows(snapshot)

print(f"\nSnapshot saved as {filename}")