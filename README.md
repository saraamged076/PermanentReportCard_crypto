# Permanent Report Card

A blockchain-based student report card system built using **Solidity**, **Web3.py**, **Python**, and **Ganache**.

The system stores student grades permanently on the blockchain with secure admin-only controls, user registration, transaction history tracking, live blockchain alerts, and Grade Coin support.

---

# Features

## Admin Features
- Add student grades
- Update student grades
- Batch add/update grades
- Mint Grade Coins
- Pause / Resume contract
- Transfer ownership to another admin
- View dashboard statistics

---

## User Features
- Register account with display name
- View personal grade
- Check ETH balance
- Check Grade Coin balance
- View personal blockchain activity history

---

## Security Features
- onlyOwner access control
- Emergency pause system
- Ownership transfer protection
- Automated security testing
- Permanent grade locking support

---

# Technologies Used

- Solidity
- Python
- Web3.py
- Ganache
- Remix IDE
- HTML / CSS / JavaScript

---

# Project Structure

```text
PermanentReportCard/
│
├── app/
│   └── main.py
│
├── Contracts/
│   └── ReportCard.sol
│
├── frontend/
│   ├── dashboard.html
│   ├── login.html
│   ├── user.html
│   ├── app.js
│   └── style.css
│
├── Scripts/
│   ├── AutoSetup.py
│   ├── ConnectContract.py
│   ├── Dashboard.py
│   ├── HistoryReport.py
│   ├── LiveAlert.py
│   ├── OwnershipTransferTest.py
│   ├── SecurityTest.py
│   └── snapshot.py
│
├── abi.json
├── bytecode.txt
├── config.json
└── README.md
```

---

# Setup Instructions

## 1. Install Requirements

Install Python packages:

```bash
pip install web3
```

---

## 2. Start Ganache

Run Ganache on:

```text
http://127.0.0.1:7545
```

---

## 3. Compile Smart Contract

Open Remix IDE.

Compile:

```text
Contracts/ReportCard.sol
```

After compiling:

- Copy ABI into `abi.json`
- Copy BYTECODE into `bytecode.txt`

---

# Deploy Smart Contract

Run:

```bash
python Scripts/AutoSetup.py
```

This script:
- Deploys the smart contract
- Saves contract address
- Adds fake student data

---

# Run Main Application

```bash
python app/main.py
```

---

# Available Scripts

## Security Test

```bash
python Scripts/SecurityTest.py
```

Checks that normal users cannot perform admin actions.

---

## Live Alert System

```bash
python Scripts/LiveAlert.py
```

Prints a live alert whenever a student grade changes.

---

## History Report

```bash
python Scripts/HistoryReport.py
```

Reads blockchain history and calculates class average grades.

---

## Ownership Transfer Test

```bash
python Scripts/OwnershipTransferTest.py
```

Tests transferring admin ownership between accounts.

---

## Balance Snapshot Exporter

```bash
python Scripts/snapshot.py
```

Exports ETH and Grade Coin balances into CSV format.

---

# Smart Contract Features

## Access Control

Only the admin can:
- Add grades
- Update grades
- Mint coins
- Pause contract
- Resume contract
- Transfer ownership

---

## Pause System

The contract supports emergency stop functionality:

- `pause()`
- `resume()`

All grade-related actions stop while paused.

---

## Ownership Transfer

Admin rights can be transferred securely using:

```solidity
transferOwnership(newAdmin)
```

---

# Example Admin Workflow

1. Start Ganache
2. Compile contract in Remix
3. Run AutoSetup script
4. Open main application
5. Login as Admin
6. Add or manage grades
7. Mint Grade Coins

---

# Example User Workflow

1. Open main application
2. Register account
3. View grade
4. Check balances
5. View activity history

---

# Authors

Permanent Report Card Team

---

# License

This project is for educational purposes only.
