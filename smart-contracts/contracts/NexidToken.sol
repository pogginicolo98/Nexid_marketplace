// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC20/ERC20.sol";

/**
 * @title The Nexid token
 */
contract NexidToken is ERC20 {
  /// @param initialSupply The initial supply of the token
  constructor(uint256 initialSupply) ERC20("Nexid", "NEX") {
    _mint(msg.sender, initialSupply);
  }
}