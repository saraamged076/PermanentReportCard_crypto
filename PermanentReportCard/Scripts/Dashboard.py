from web3 import Web3
import json
from collections import Counter

# connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

print("Connected:", web3.is_connected())

# load config
with open("config.json") as f:
    config = json.load(f)

contract_address = config["contract_address"]

# load ABI
with open("abi.json") as f:
    abi = json.load(f)

# connect contract
contract = web3.eth.contract(address=contract_address, abi=abi)


# 1. Total Students (approx)
# we will scan accounts and check who has data

students_count = 0

for acc in web3.eth.accounts:
    name, grade = contract.functions.getGrade(acc).call()
    if name != "" or grade != 0:
        students_count += 1


# 2. Total Coins

total_coins = contract.functions.totalSupply().call()

# 3. Total Transactions

latest_block = web3.eth.block_number
tx_count = 0


# 4. Top Active Users

activity = []

for i in range(latest_block + 1):
    block = web3.eth.get_block(i, full_transactions=True)

    tx_count += len(block.transactions)

    for tx in block.transactions:
        activity.append(tx['from'])

# count activity
counter = Counter(activity)
top_users = counter.most_common(3)


# PRINT RESULTS

print("\n===== ADMIN DASHBOARD =====")

print(f"Total Students: {students_count}")
print(f"Total Coins Minted: {total_coins}")
print(f"Total Transactions: {tx_count}")

print("\nTop 3 Active Users:")
for addr, count in top_users:
    print(f"{addr} → {count} transactions")