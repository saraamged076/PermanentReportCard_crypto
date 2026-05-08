from web3 import Web3
import json
from collections import Counter

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


# ================== 1. TOTAL STUDENTS ==================
grade_events = contract.events.GradeSet().get_logs()

students = set()

for event in grade_events:
    students.add(event['args']['student'])

students_count = len(students)

# ================== 2. TOTAL COINS ==================

mint_events = contract.events.CoinsMinted().get_logs()

total_coins = 0

for event in mint_events:
    total_coins += event['args']['amount']


# ================== 3. TOTAL CONTRACT TRANSACTIONS ==================

latest_block = web3.eth.block_number
tx_count = 0

# ================== 4. TOP ACTIVE USERS ==================

activity = []

for i in range(latest_block + 1):
    block = web3.eth.get_block(i, full_transactions=True)

    for tx in block.transactions:

        # check if tx is to our contract
        if tx['to'] and tx['to'].lower() == contract_address.lower():
            tx_count += 1
            activity.append(tx['from'])


# count activity
counter = Counter(activity)
top_users = counter.most_common(3)


# ================== PRINT ==================

print("\n===== ADMIN DASHBOARD =====")

print(f"Total Students: {students_count}")
print(f"Total Coins Minted: {total_coins}")
print(f"Total Contract Transactions: {tx_count}")

print("\nTop 3 Active Users:")
for addr, count in top_users:
    print(f"{addr} → {count} actions")