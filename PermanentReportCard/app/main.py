from web3 import Web3
import json
# Connect to Ganache local blockchain
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Admin account (first Ganache account)
admin_address = web3.eth.accounts[0]

# Check connection status
print("Connected:", web3.is_connected())

# Contract address (replace with your deployed contract address)
with open("config.json") as f:
    config = json.load(f)

contract_address = config["contract_address"]

# ABI 
with open("abi.json") as f:
    abi = json.load(f)
    

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)
##############################user menu function#####################################
def user_menu(user_name, user_address):
    while True:
        print(f"\n=== User Menu === (Welcome {user_name})")
        print("1. View Grade")
        print("2. Check Balance (ETH + Coin)")
        print("3. Activity History")
        print("4. Back")

        user_choice = input("Choose an option: ")
        # ===== View Grade =====
        if user_choice == "1":
            try:
                addr = Web3.to_checksum_address(user_address)
                user_name, grade = contract.functions.getGrade(addr).call()
                print("\n--- Student Info ---")
                print(f"Name : {user_name}")
                print(f"Grade: {grade}")
                # print("Registered name:", contract.functions.userNames(addr).call())
                # print("Grade result:", contract.functions.getGrade(addr).call())
            except Exception as e:
                print(" Error:", e) 

        # ===== Balance =====
        elif user_choice == "2":
            try:
                addr = Web3.to_checksum_address(user_address)
                coin = contract.functions.getBalance(addr).call()
                eth = web3.eth.get_balance(addr)

                print("\n=== Balance ===")
                print(f"Address: {addr}")
                print(f"ETH  : {web3.from_wei(eth, 'ether')} ETH")
                print(f"Coin : {coin} GC")

            except Exception as e:
                print(" Error:", e)

        # ===== Activity History =====
        elif user_choice == "3":
            try:
                        addr = Web3.to_checksum_address(input("Enter address: ").strip())
                        latest_block = web3.eth.block_number
                        print("\n=== Activity History ===")
                        print("Block | Action | Value")
                        found = False
                        for i in range(latest_block + 1):
                            block = web3.eth.get_block(i, full_transactions=True)
                            for tx in block.transactions:
                                if tx['from'] == addr or tx['to'] == addr:
                                    value = web3.from_wei(tx['value'], 'ether')
                                    if tx['to'] == contract.address:
                                        action = "Interacted with Contract"
                                    elif tx['to'] is None:
                                        action = "Contract Deployment"
                                    elif value > 0:
                                        action = "ETH Transfer"
                                    else:
                                        action = "Transaction"
                                    print(f"{i} | {action} | {value}")
                                    found = True
                        if not found:
                            print("No activity found.")

            except Exception as e:
                 print("Error:", e)
                                     
        elif user_choice == "4":
            break     
#################admin menu function#####################
def admin_menu(password, admin_address):

    if password != "admin123":
        print("Wrong password")
        return

    contract_admin = contract.functions.getAdmin().call()
    if admin_address != contract_admin:
        print("Not authorized as admin")
        return

    while True:
        print("\n=== Admin Menu ===")
        print("1. Add Grade")
        print("2. Update Grade")
        print("3. Mint Coins")
        print("4. Batch Add Grades")
        print("5. Back")

        admin_choice = input("Choose: ")
     # ================= ADD =================
    
        if admin_choice == "1":
            accounts = web3.eth.accounts
            for i, acc in enumerate(accounts):
                print(f"{i}. {acc}")
            idx = int(input("Choose student index: "))
            student = Web3.to_checksum_address(accounts[idx])
            try:
                # check if registered
                name = contract.functions.userNames(student).call()
                if name == "":
                    print("This user is not registered! Ask them to register first.")
                    continue
                # check if already has grade
                existing_name, existing_grade = contract.functions.getGrade(student).call()

                if existing_grade != 0:
                    print(f"{name} already has grade ({existing_grade})\n Use Update instead.")
                    continue

                print(f"Student Name: {name}")

                grade = int(input("Enter grade: "))

                if grade < 0 or grade > 100:
                    print("Invalid grade")
                    continue

                # send tx (name from register)
                tx = contract.functions.setGrade(
                    student, name, grade
                ).transact({'from': admin_address})

                web3.eth.wait_for_transaction_receipt(tx)

                print("Grade added successfully!")

            except Exception as e:
                print("Error:", e)
    # ================= UPDATE ================= 
        elif admin_choice == "2":
            
            user_address = input("Enter student address: ")
            try:
            # check if student exists
                    name, grade = contract.functions.getGrade(user_address).call()
                    if name == "" and grade == 0:
                     print(" Student does not exist!you should add Student first.")
                    else:
                        print(f"Current Name: {name},\n Current Grade: {grade}")
                        new_grade = int(input("Enter new grade: "))
                        if new_grade < 0 or new_grade > 100:
                            print("Invalid grade")
                            continue
                        else:
                            tx = contract.functions.setGrade(
                               name, new_grade).transact({'from': admin_address})
                            web3.eth.wait_for_transaction_receipt(tx)
                            print(" Grade updated successfully!")
            except Exception as e:
                print("Error:", e)
                    # ================= MINT =================
        elif admin_choice == "3":
             to = Web3.to_checksum_address(input("Enter address: ").strip())
             try:
                # check if student exists
                name, grade = contract.functions.getGrade(to).call()
                if name == "" and grade == 0:
                     print("This student does not exist! Add student first.")
                else:
                     print(f"Student: {name}, Grade: {grade}")
                     # mint coins
                     amount = int(input("Enter amount: "))
                     if amount <= 0:
                            print("Invalid amount")
                            continue
                     else:
                            tx = contract.functions.mint(to, amount).transact({
                            'from': admin_address
                            })
                            web3.eth.wait_for_transaction_receipt(tx)
                            print("Coins minted successfully!")
                            print(f"New balance of {name}: {contract.functions.getBalance(to).call()}")
             except Exception as e:
                    print("Error:", e)        
                    # ================= BATCH ADD =================
        elif admin_choice == "4":
             try:
                    n = int(input("How many students? "))
                    students = []
                    names = []
                    grades = []
                    for i in range(n):
                            print(f"\nStudent {i+1}")

                            addr = input("Enter address: ").strip()
                            name = input("Enter name: ").strip()
                            grade = int(input("Enter grade: "))
                        # ===== VALIDATION =====
                            if addr == "" or name == "":
                                print(" Invalid input, cancelling batch")
                                break
                            if grade < 0 or grade > 100:
                                print(" Invalid grade, cancelling batch")
                                break
                        # check if student already exists
                            existing_name, existing_grade = contract.functions.getGrade(addr).call()
                            if existing_name != "" or existing_grade != 0:
                              print(f"Student already exists! Use Update instead.")
                              break
                        # ===== ADD =====
                            students.append(addr)
                            names.append(name)
                            grades.append(grade)
                    else:
                    # final confirmation before batch adding
                        tx = contract.functions.batchSetGrades(
                            students, names, grades
                        ).transact({'from': admin_address})

                        web3.eth.wait_for_transaction_receipt(tx)

                        print(" Batch added successfully!")

             except Exception as e:
                    print("Error:", e)
                 # ================= BACK =================
        elif admin_choice == "5":
            break

        else:
            print("Invalid choice")
################################################################

# Function to display menu options
def main_menu():
    print("\n=== Welcome to Report Card System ===")
    print("1. User")
    print("2. Admin")
    print("3. Show Admin")
    print("4. Exit")

# Main program loop
while True:
    main_menu()
    choice = input("Choose an option: ")

    # ================= USER =================
    if choice == "1":
        # List available accounts
        accounts = web3.eth.accounts
        print("\nAvailable accounts:")
        for i, acc in enumerate(accounts):
            print(f"{i}. {acc}")

        try:
            index = int(input("Choose account index: "))
            user_address = accounts[index]
        except:
            print("Invalid choice")
            continue

        print(f"\nUsing address: {user_address}")

        try:
            name = contract.functions.userNames(user_address).call()
            # =====if not registered=====
            if name == "":
                print("You are not registered.")
                register = input("Do you want to register? (y/n): ")

                if register.lower() == "y":
                    user_name = input("Enter your name: ").strip()

                    tx = contract.functions.registerUser(user_name).transact({
                        'from': user_address
                    })
                    web3.eth.wait_for_transaction_receipt(tx)
                    print("Registered successfully!")
                    name = user_name
                else:
                    continue

            # ===== user menu =====
            user_menu(name, user_address)

        except Exception as e:
            print(" Error:", e)
   #######################################################################
    elif choice == "2":
        password = input("Enter admin password: ")
        admin_address = input("Enter admin address: ")
        admin_menu(password, admin_address)
 
   ###################################################################### 
   # Option 3: Show Admin
    elif choice == "3":
          admin = contract.functions.getAdmin().call()
          print(f"Admin address: {admin}")
   #######################################################################   
    elif choice == "4":
            print("Goodbye!")
            break

        # Invalid input handling
    else:
            print("Invalid choice, please try again.")
                     

#     # Option 5: Check Balance
#     elif choice == "5":
#             address = input("Enter address: ")
#             try:
#                 balance = contract.functions.getBalance(address).call()
#                 print(f" Coin Balance: {balance}")

#             except Exception as e:
#                 print("Error:", e)

####################################################

                
