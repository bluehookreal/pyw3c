pragma solidity ^0.4.24;


contract Yaofan {
    uint256 constant public giveme_min = 0.1 ether;
    uint256 public goodman_count = 0;
    mapping (address => bool) public list;
    address public admin;

    constructor(address god) public {
        admin = god;
    }

    function givemoney(address goodman) payable public {
        require(msg.value >= giveme_min && list[goodman] == false);
        list[goodman] = true;
        goodman_count++;
    }

    function payall() public {
        admin.transfer(this.balance);
    }
}