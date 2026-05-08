# Permanent Report Card

## Project Idea
A blockchain-based permanent student report card system using Solidity and Web3.py.

Student grades are stored securely on the blockchain with admin-controlled access.

---

# Requirements

- Python 3
- Ganache
- Web3.py
- Solidity Compiler
- Remix IDE

---

# Setup Instructions

## 1. Start Ganache

Open Ganache and start a local blockchain at:

http://127.0.0.1:7545

---

## 2. Compile Smart Contract

Open Remix IDE.

Compile:

Contracts/ReportCard.sol

Copy:
- ABI -> abi.json
- BYTECODE -> bytecode.txt

---

## 3. Deploy Contract

Run:

```bash
python Scripts/AutoSetup.py