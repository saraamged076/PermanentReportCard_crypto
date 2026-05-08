import tkinter as tk
from web3 import Web3
import json

# ================= CONNECT =================
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

with open("config.json") as f:
    contract_address = json.load(f)["contract_address"]

with open("abi.json") as f:
    abi = json.load(f)

contract = web3.eth.contract(address=contract_address, abi=abi)
accounts = web3.eth.accounts

current_user = {"address": None, "name": None}
admin_data = {"action": None, "student": None}

# ================= ROOT =================
root = tk.Tk()
root.title("Report Card System")
root.geometry("500x550")

frames = {}
for name in [
    "main","accounts","register","user_menu","result",
    "admin_login","admin_menu","select_student","admin_action"
]:
    frame = tk.Frame(root)
    frame.grid(row=0,column=0,sticky="nsew")
    frames[name] = frame

def show(name):
    frames[name].tkraise()

# ================= MAIN =================
tk.Label(frames["main"], text="=== Welcome to Report Card System ===", font=("Arial",14)).pack(pady=20)

tk.Button(frames["main"], text="1. User", width=25,
          command=lambda: show("accounts")).pack(pady=5)

tk.Button(frames["main"], text="2. Admin", width=25,
          command=lambda: show("admin_login")).pack(pady=5)

tk.Button(frames["main"], text="3. Show Admin", width=25,
          command=lambda: show_admin()).pack(pady=5)

tk.Button(frames["main"], text="4. Exit", width=25,
          command=root.quit).pack(pady=5)

# ================= SHOW ADMIN =================
def show_admin():
    try:
        admin = contract.functions.getAdmin().call()
        result_text.set(f"Admin address:\n{admin}")
        show("result")
    except Exception as e:
        result_text.set(str(e))
        show("result")

# ================= ACCOUNTS =================
listbox = tk.Listbox(frames["accounts"], width=60)
listbox.pack()

for i, acc in enumerate(accounts):
    listbox.insert(tk.END, f"{i} - {acc}")

def select_account():
    try:
        index = listbox.curselection()[0]
    except:
        return

    addr = accounts[index]
    current_user["address"] = addr

    try:
        name, _ = contract.functions.getGrade(addr).call()
        if name == "":
            show("register")
        else:
            current_user["name"] = name
            load_user_menu()
            show("user_menu")
    except:
        show("register")

tk.Button(frames["accounts"], text="Select", command=select_account).pack(pady=10)

# ================= REGISTER =================
tk.Label(frames["register"], text="Enter Name").pack(pady=10)
name_entry = tk.Entry(frames["register"])
name_entry.pack()

def do_register():
    try:
        addr = current_user["address"]
        name = name_entry.get()

        tx = contract.functions.registerUser(name).transact({'from': addr})
        web3.eth.wait_for_transaction_receipt(tx)

        current_user["name"] = name
        load_user_menu()
        show("user_menu")

    except Exception as e:
        result_text.set(f"{str(e)}")
        show("result")

tk.Button(frames["register"], text="Register", command=do_register).pack(pady=10)

# ================= USER MENU =================
menu_label = tk.Label(frames["user_menu"], text="")
menu_label.pack(pady=10)

def load_user_menu():
    menu_label.config(text=f"=== User Menu ===\nWelcome {current_user['name']}")

def view_grade():
    try:
        addr = current_user["address"]
        name, grade = contract.functions.getGrade(addr).call()
        result_text.set(f"Name: {name}\nGrade: {grade}")
        show("result")
    except Exception as e:
        result_text.set(str(e))
        show("result")

def balance():
    try:
        addr = current_user["address"]
        coin = contract.functions.getBalance(addr).call()
        eth = web3.from_wei(web3.eth.get_balance(addr), "ether")
        result_text.set(f"ETH: {eth}\nCoin: {coin}")
        show("result")
    except Exception as e:
        result_text.set(str(e))
        show("result")

tk.Button(frames["user_menu"], text="1. View Grade", command=view_grade).pack(pady=5)
tk.Button(frames["user_menu"], text="2. Balance", command=balance).pack(pady=5)
tk.Button(frames["user_menu"], text="3. Back",
          command=lambda: show("main")).pack(pady=5)

# ================= RESULT =================
result_text = tk.StringVar()
tk.Label(frames["result"], textvariable=result_text).pack(pady=20)
tk.Button(frames["result"], text="Back",
          command=lambda: show("main")).pack()

# ================= ADMIN LOGIN =================
error_label = tk.Label(frames["admin_login"], fg="red")
error_label.pack(pady=5)

tk.Label(frames["admin_login"], text="Password").pack()
pass_entry = tk.Entry(frames["admin_login"], show="*", width=30)
pass_entry.pack(pady=5)

tk.Label(frames["admin_login"], text="Admin Address").pack()
admin_entry = tk.Entry(frames["admin_login"], width=50)
admin_entry.pack(pady=5)

def admin_login():
    password = pass_entry.get().strip()
    address = admin_entry.get().strip()

    if password != "admin123":
        error_label.config(text="Wrong password")
        return

    try:
        entered_admin = Web3.to_checksum_address(address)
        real_admin = contract.functions.getAdmin().call()

        if entered_admin.lower() != real_admin.lower():
            error_label.config(text=" Not admin")
            return

        error_label.config(text="")
        show("admin_menu")

    except:
        error_label.config(text="Invalid address")

tk.Button(frames["admin_login"], text="Login", command=admin_login).pack(pady=10)

# ================= ADMIN MENU =================
tk.Label(frames["admin_menu"], text="=== Admin Menu ===").pack(pady=10)

def go_action(action):
    admin_data["action"] = action

    if action in ["add","update","mint","batch"]:
        load_students()
        show("select_student")
    else:
        show("admin_action")

buttons = [
    ("1. Add Grade","add"),
    ("2. Update Grade","update"),
    ("3. Mint Coins","mint"),
    ("4. Batch Add Grades","batch"),
    ("5. Pause Contract","pause"),
    ("6. Resume Contract","resume"),
    ("7. Transfer Ownership","transfer"),
]

for text, act in buttons:
    tk.Button(frames["admin_menu"], text=text,
              command=lambda a=act: go_action(a)).pack(pady=3)

tk.Button(frames["admin_menu"], text="8. Back",
          command=lambda: show("main")).pack(pady=5)

# ================= SELECT STUDENT =================
student_list = tk.Listbox(frames["select_student"], width=60)
student_list.pack()

def load_students():
    student_list.delete(0, tk.END)
    for i, acc in enumerate(accounts):
        student_list.insert(tk.END, f"{i} - {acc}")

def choose_student():
    try:
        index = student_list.curselection()[0]
    except:
        return

    admin_data["student"] = accounts[index]
    show("admin_action")

tk.Button(frames["select_student"], text="Select",
          command=choose_student).pack(pady=10)

# ================= ADMIN ACTION =================
action_label = tk.Label(frames["admin_action"], text="")
action_label.pack()

input_entry = tk.Entry(frames["admin_action"])
input_entry.pack(pady=10)

result_admin = tk.Label(frames["admin_action"], text="")
result_admin.pack()

def do_action():
    admin = contract.functions.getAdmin().call()

    try:
        action = admin_data["action"]

        if action in ["add","update","mint"]:
            addr = admin_data["student"]
            name, grade = contract.functions.getGrade(addr).call()

            if name == "":
                result_admin.config(text="Student not registered")
                return

            val = int(input_entry.get())

            if action == "add":
                if grade != 0:
                    result_admin.config(text="⚠ Already has grade")
                    return
                tx = contract.functions.setGrade(addr, val).transact({'from': admin})

            elif action == "update":
                if grade == 0:
                    result_admin.config(text="⚠ No grade yet")
                    return
                tx = contract.functions.setGrade(addr, val).transact({'from': admin})

            elif action == "mint":
                tx = contract.functions.mint(addr, val).transact({'from': admin})

        elif action == "batch":
            data = input_entry.get()
            try:
                addresses_str, grades_str = data.split("|")

                addr_list = [Web3.to_checksum_address(a.strip()) for a in addresses_str.split(",")]
                grade_list = [int(g.strip()) for g in grades_str.split(",")]

                tx = contract.functions.batchSetGrades(addr_list, grade_list).transact({'from': admin})
            except:
                result_admin.config(text="Format: addr1,addr2 | grade1,grade2")
                return

        elif action == "pause":
            tx = contract.functions.pause().transact({'from': admin})

        elif action == "resume":
            tx = contract.functions.resume().transact({'from': admin})

        elif action == "transfer":
            new_admin = Web3.to_checksum_address(input_entry.get())
            tx = contract.functions.transferOwnership(new_admin).transact({'from': admin})

        web3.eth.wait_for_transaction_receipt(tx)
        result_admin.config(text="Success")

    except Exception as e:
        msg = str(e).lower()

        if "paused" in msg:
            result_admin.config(text="⚠ Contract is paused")
        elif "not admin" in msg:
            result_admin.config(text="Only admin allowed")
        else:
            result_admin.config(text=f"{msg}")

tk.Button(frames["admin_action"], text="Submit", command=do_action).pack()
tk.Button(frames["admin_action"], text="Back",
          command=lambda: show("admin_menu")).pack()

# ================= START =================
show("main")
root.mainloop()