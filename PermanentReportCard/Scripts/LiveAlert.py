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
# listen only for GradeSet event
event_filter = contract.events.GradeSet.create_filter(
    from_block='latest'
)

print("Listening for REAL grade changes...")

while True:

    for event in event_filter.get_new_entries():

        student = event['args']['student']
        grade = event['args']['grade']

        print("\n🚨 ALERT: A grade change just happened!")
        print("Student:", student)
        print("New Grade:", grade)

    time.sleep(2)