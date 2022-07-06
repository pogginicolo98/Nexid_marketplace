// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../interfaces/INFTSeller.sol";
import "./NexidToken.sol";
import "./NexidNFT.sol";


/**
 * @title The NFT seller
 * @notice The NFTSeller allows the sale of ERC721 tokens for ERC20 tokens
 */
abstract contract NFTSeller is INFTSeller {
  address payable owner;
  NexidToken public nexidToken;
  NexidNFT public nexidNFT;
  uint256 public price;

  /**
   * @param _nexidToken NexidToken.sol address
   * @param _nexidNFT NexidNFT.sol address
   * @param _price NexidNFT priced in NexidToken
   */
  constructor(NexidToken _nexidToken, NexidNFT _nexidNFT, uint256 _price) {
    owner = payable(msg.sender);
    nexidToken = _nexidToken;
    nexidNFT = _nexidNFT;
    price = _price;
  }

  /// @inheritdoc INFTSeller
  function purchase(uint256 tokenId)
    external
    override
    onlyNexidNFTAvailable(tokenId)
    onlyNexidTokenApproved()
    onlySufficientBalance()
  {
    nexidToken.transferFrom(msg.sender, address(this), price);
    nexidNFT.transferFrom(address(this), msg.sender, tokenId);
    emit ItemPurchased(msg.sender, tokenId);
  }

  /// @inheritdoc INFTSeller
  function withdraw(uint256 amount)
    external
    override
    onlyOwner()
    onlyAvailableBalance(amount)
  {
    nexidToken.transfer(owner, amount);
    emit FundsWithdrawn(owner, amount);
  }

  /**
   * @dev Allows execution only if the provided token ID belongs to the NFTSeller
   *
   * @param tokenId The token ID of the NFT
   */
  modifier onlyNexidNFTAvailable(uint256 tokenId) {
    require(
      nexidNFT.ownerOf(tokenId) == address(this),
      "NFT not for sale."
    );
    _;
  }

  /// @dev Allows execution only if the NFTSeller is allowed to spend caller's Nexid tokens
  modifier onlyNexidTokenApproved() {
    require(
      nexidToken.allowance(msg.sender, address(this)) >= price,
      "NexidToken not approved."
    );
    _;
  }

  /// @dev Allows execution only if the caller has a sufficient Nexid token balance
  modifier onlySufficientBalance() {
    require(
      nexidToken.balanceOf(msg.sender) >= price,
      "Not enough Nexid tokens."
    );
    _;
  }

  /// @dev Allows execution only if the caller is the owner
  modifier onlyOwner() {
    require(
      msg.sender == owner,
      "Only owner can call this function."
    );
    _;
  }

  /**
   * @dev Allows execution only if the NFTSeller has at least the provided amount of Nexid tokens.
   *
   * @param amount The amount provided for withdrawal
   */
  modifier onlyAvailableBalance(uint256 amount) {
    require(
      amount <= nexidToken.balanceOf(address(this)),
      "The amount exceeds the available balance."
    );
    _;
  }
}


/**
 * @title The seller of Nexid NFTs
 */
contract NexidSeller is NFTSeller {
  /*
   * @param nexidToken NexidToken.sol address
   * @param nexidNFT NexidNFT.sol address
   * @param price NexidNFT priced in NexidToken
   */
  constructor(NexidToken nexidToken, NexidNFT nexidNFT, uint256 price) NFTSeller(nexidToken, nexidNFT, price) {}
}
