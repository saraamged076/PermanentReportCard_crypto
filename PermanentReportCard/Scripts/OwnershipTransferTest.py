from web3 import Web3
import json

# ================= CONNECT =================
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

print("Connected:", web3.is_connected())

# ================= LOAD =================
with open("config.json") as f:
    config = json.load(f)

with open("abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(
    address=config["contract_address"],
    abi=abi
)

# ================= ACCOUNTS =================
old_admin = web3.eth.accounts[0]
new_admin = web3.eth.accounts[1]
student = web3.eth.accounts[2]

# ================= STEP 1 =================
print("\nSTEP 1: Old admin action")

try:

    tx = contract.functions.mint(
        student,
        10
    ).transact({
        'from': old_admin
    })

    web3.eth.wait_for_transaction_receipt(tx)

    print("Old admin action SUCCESS")

except Exception as e:

    print("FAILED:", e)

# ================= STEP 2 =================
print("\nSTEP 2: Transfer ownership")

try:

    tx = contract.functions.transferOwnership(
        new_admin
    ).transact({
        'from': old_admin
    })

    web3.eth.wait_for_transaction_receipt(tx)

    print("Ownership transferred!")

except Exception as e:

    print("FAILED:", e)

# ================= STEP 3 =================
print("\nSTEP 3: Old admin should FAIL")

try:

    tx = contract.functions.mint(
        student,
        10
    ).transact({
        'from': old_admin
    })

    web3.eth.wait_for_transaction_receipt(tx)

    print("ERROR: old admin still works!")

except:

    print("PASS: old admin blocked")

# ================= STEP 4 =================
print("\nSTEP 4: New admin should work")

try:

    tx = contract.functions.mint(
        student,
        10
    ).transact({
        'from': new_admin
    })

    web3.eth.wait_for_transaction_receipt(tx)

    print("PASS: new admin works")

except Exception as e:

    print("FAILED:", e)