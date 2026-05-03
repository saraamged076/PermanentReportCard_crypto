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

total = 0
count = 0

for acc in web3.eth.accounts:
    name, grade = contract.functions.getGrade(acc).call()

    if name != "" or grade != 0:
        total += grade
        count += 1

if count > 0:
    avg = total / count
else:
    avg = 0

print("\n=== CLASS REPORT ===")
print(f"Students: {count}")
print(f"Average Grade: {avg:.2f}")