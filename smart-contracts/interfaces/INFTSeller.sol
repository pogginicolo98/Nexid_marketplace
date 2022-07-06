// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


/**
 * @title The interface for the NFTSeller
 * @notice The NFTSeller allows the sale of ERC721 tokens for ERC20 tokens
 */
interface INFTSeller {
  /**
   * @notice Emitted when an NFT has been sold
   *
   * @param by The address that purchased the NFT
   * @param tokenId The token ID of the NFT sold
   */
  event ItemPurchased(address by, uint256 tokenId);

  /**
   * @notice Emitted when funds are withdrawn
   *
   * @param by The address that withdrew the funds
   * @param amount The amount withdrawn
   */
  event FundsWithdrawn(address by, uint256 amount);

  /**
   * @notice It transfers the chosen NFT to the caller for the set amount of tokens
   * @dev The NFT must belong to the NFTSeller
   * @dev The caller must have approved the NFTSeller for the token transfer
   * @dev The caller must have at least the required amount of tokens
   *
   * @param tokenId The token ID of the NFT put up for sale
   */
  function purchase(uint256 tokenId) external;

  /**
   * @notice It transfers the provided amount of the raised funds to the owner
   * @dev The caller must be the owner
   * @dev The amount can be at most the total of available funds
   *
   * @param amount The amount of token to transfer
   */
  function withdraw(uint256 amount) external;
}
