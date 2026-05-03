// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReportCard {

    address public admin;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == admin, "Not admin");
        _;
    }

    // ================== EVENTS ==================
    event UserRegistered(address user, string name);
    event GradeSet(address student, string name, uint grade);
    event CoinsMinted(address to, uint amount);
    event Transfer(address from, address to, uint amount);

    // ================== STUDENTS ==================
    struct Student {
        string name;
        uint grade;
    }

    mapping(address => Student) public students;

    function setGrade(address student, string memory name, uint grade) public onlyOwner {
        require(student != address(0), "Invalid address");
        require(bytes(name).length > 0, "Invalid name");
        require(grade <= 100, "Grade must be <= 100");

        students[student] = Student(name, grade);

        emit GradeSet(student, name, grade);
    }

    function getGrade(address student) public view returns(string memory, uint) {
        string memory name = userNames[student];

        //if not registered
        if (bytes(name).length == 0) {
            name = students[student].name;
        }
        return (name, students[student].grade);
    }
    // ================== USERS ==================
    mapping(address => string) public userNames;
    mapping(address => bool) public isRegistered;

    function registerUser(string memory name) public {
        require(!isRegistered[msg.sender], "Already registered");

        userNames[msg.sender] = name;
        isRegistered[msg.sender] = true;

        
        students[msg.sender].name = name;

        emit UserRegistered(msg.sender, name);
    }

    // ================== ADMIN ==================
    function getAdmin() public view returns(address) {
        return admin;
    }

    // ================== COIN ==================
    string public coinName = "GradeCoin";
    string public coinSymbol = "GC";
    uint public totalSupply;

    mapping(address => uint) public balances;

    function mint(address to, uint amount) public onlyOwner {
        require(to != address(0), "Invalid address");
        require(amount > 0, "Amount must be > 0");

        balances[to] += amount;
        totalSupply += amount;

        emit CoinsMinted(to, amount);
    }

    function getBalance(address user) public view returns(uint) {
        return balances[user];
    }

    function transfer(address to, uint amount) public {
        require(balances[msg.sender] >= amount, "Not enough balance");
        require(to != address(0), "Invalid address");
        require(amount > 0, "Invalid amount");

        balances[msg.sender] -= amount;
        balances[to] += amount;

        emit Transfer(msg.sender, to, amount);
    }

    // ================== BATCH ==================
    function batchSetGrades(
        address[] memory _students,
        string[] memory _names,
        uint[] memory _grades
    )
    public onlyOwner {

        require(
            _students.length == _names.length &&
            _names.length == _grades.length,
            "Array length mismatch"
        );

        for (uint i = 0; i < _students.length; i++) {
            require(_students[i] != address(0), "Invalid address");
            require(bytes(_names[i]).length > 0, "Invalid name");
            require(_grades[i] <= 100, "Invalid grade");

            students[_students[i]] = Student(_names[i], _grades[i]);

            emit GradeSet(_students[i], _names[i], _grades[i]);
        }
    }
}