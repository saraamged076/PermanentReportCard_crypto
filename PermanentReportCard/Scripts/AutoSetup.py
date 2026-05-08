from web3 import Web3
import json

# ================= CONNECT =================
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

print("Connected:", web3.is_connected())

admin = web3.eth.accounts[0]

# ================= LOAD ABI =================
with open("abi.json") as f:
    abi = json.load(f)

# ================= LOAD BYTECODE =================
with open("bytecode.txt") as f:
    bytecode = f.read().strip()

# ================= DEPLOY =================
contract = web3.eth.contract(abi=abi, bytecode=bytecode)

print(" Deploying contract...")

tx_hash = contract.constructor().transact({
    'from': admin
})

receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = receipt.contractAddress

print("Contract deployed at:", contract_address)

# ================= SAVE ADDRESS =================
with open("config.json", "w") as f:
    json.dump({"contract_address": contract_address}, f)

print("Address saved!")

# ================= CONNECT TO CONTRACT =================
contract = web3.eth.contract(address=contract_address, abi=abi)

# ================= FAKE DATA =================
students = [
    (web3.eth.accounts[1], "Sara", 95),
    (web3.eth.accounts[2], "Ali", 88),
    (web3.eth.accounts[3], "Mona", 92),
]

print("\nAdding fake data...")

# ================= ADD DATA =================
for student, name, grade in students:
    try:
        tx = contract.functions.setGrade(
            student, name, grade
        ).transact({'from': admin})

        web3.eth.wait_for_transaction_receipt(tx)

        print(f" {name} added!")

    except Exception as e:
        print("Error:", e)

print("\nProject is READY TO USE!")