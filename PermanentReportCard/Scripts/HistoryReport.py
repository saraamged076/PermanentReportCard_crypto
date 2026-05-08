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

# ===== READ BLOCKCHAIN HISTORY =====
events = contract.events.GradeSet().get_logs(
    from_block=0,
    to_block='latest'
)

latest_grades = {}

for event in events:

    student = event['args']['student']
    grade = event['args']['grade']

    latest_grades[student] = grade

# ===== CALCULATE AVERAGE =====
for student, grade in latest_grades.items():

    total += grade
    count += 1