// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReportCard {

    address public admin;
    bool public paused;

    uint public totalStudents; 

    constructor() {
        admin = msg.sender;
        paused = false;
    }

    // ================== MODIFIERS ==================
    modifier onlyOwner() {
        require(msg.sender == admin, "Not admin");
        _;
    }

    modifier whenNotPaused() {
        require(!paused, "Contract is paused");
        _;
    }

    // ================== EVENTS ==================
    event UserRegistered(address user, string name);
    event GradeSet(address student, string name, uint grade);
    event CoinsMinted(address to, uint amount);
    event Transfer(address from, address to, uint amount);
    event OwnershipTransferred(address oldAdmin, address newAdmin);
    event Paused();
    event Resumed();

    // ================== STUDENTS ==================
    struct Student {
        string name;
        uint grade;
    }

    mapping(address => Student) public students;

    // ================== USERS ==================
    mapping(address => string) public userNames;
    mapping(address => bool) public isRegistered;

    function registerUser(string memory name) public whenNotPaused {
        require(!isRegistered[msg.sender], "Already registered");
        require(bytes(name).length > 0, "Invalid name");

        userNames[msg.sender] = name;
        isRegistered[msg.sender] = true;

        emit UserRegistered(msg.sender, name);
    }

    // ================== GRADES ==================
    function setGrade(
        address student,
        uint grade
    )
    public onlyOwner whenNotPaused
    {
        require(student != address(0), "Invalid address");
        require(isRegistered[student], "User not registered");
        require(grade <= 100, "Grade must be <= 100");

        // لو أول مرة يتسجل
        if (students[student].grade == 0) {
            totalStudents++;
        }

        string memory name = userNames[student];

        students[student] = Student(name, grade);

        emit GradeSet(student, name, grade);
    }

    function getGrade(address student)
        public view
        returns(string memory, uint)
    {
        string memory name = userNames[student];
        return (name, students[student].grade);
    }

    // ================== ADMIN ==================
    function getAdmin() public view returns(address) {
        return admin;
    }

    function transferOwnership(address newAdmin) public onlyOwner {
        require(newAdmin != address(0), "Invalid address");

        address old = admin;
        admin = newAdmin;

        emit OwnershipTransferred(old, newAdmin);
    }

    // ================== PAUSE ==================
    function pause() public onlyOwner {
        require(!paused, "Already paused");
        paused = true;
        emit Paused();
    }

    function resume() public onlyOwner {
        require(paused, "Not paused");
        paused = false;
        emit Resumed();
    }

    // ================== COIN ==================
    string public coinName = "GradeCoin";
    string public coinSymbol = "GC";
    uint public totalSupply;

    mapping(address => uint) public balances;

    function mint(address to, uint amount)
        public onlyOwner whenNotPaused
    {
        require(to != address(0), "Invalid address");
        require(isRegistered[to], "User not registered");
        require(amount > 0, "Amount must be > 0");

        balances[to] += amount;
        totalSupply += amount;

        emit CoinsMinted(to, amount);
    }

    function getBalance(address user) public view returns(uint) {
        return balances[user];
    }

    function transfer(address to, uint amount)
        public whenNotPaused
    {
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
        uint[] memory _grades
    )
    public onlyOwner whenNotPaused
    {
        require(
            _students.length == _grades.length,
            "Array length mismatch"
        );

        for (uint i = 0; i < _students.length; i++) {
            require(_students[i] != address(0), "Invalid address");
            require(isRegistered[_students[i]], "User not registered");
            require(_grades[i] <= 100, "Invalid grade");

            if (students[_students[i]].grade == 0) {
                totalStudents++;
            }

            string memory name = userNames[_students[i]];

            students[_students[i]] = Student(name, _grades[i]);

            emit GradeSet(_students[i], name, _grades[i]);
        }
    }
}