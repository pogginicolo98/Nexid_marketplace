// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/utils/Counters.sol";


/**
 * @title The Nexid NFT
 * @notice Implementation of Openzeppelin's ERC721Enumerable and ERC721URIStorage contracts
 */
contract NexidNFT is ERC721Enumerable, ERC721URIStorage {
  using Counters for Counters.Counter;
  Counters.Counter private _tokenIds;
  address payable public owner;

  constructor() ERC721("Nexid NFT", "ID") {
    owner = payable(msg.sender);
  }

  function _beforeTokenTransfer(address from, address to, uint256 tokenId)
    internal
    override(ERC721, ERC721Enumerable)
  {
    super._beforeTokenTransfer(from, to, tokenId);
  }

  function _burn(uint256 tokenId)
    internal
    override(ERC721, ERC721URIStorage)
  {
    super._burn(tokenId);
  }

  function supportsInterface(bytes4 interfaceId)
    public
    view
    override(ERC721, ERC721Enumerable)
    returns (bool)
  {
    return super.supportsInterface(interfaceId);
  }

  function tokenURI(uint256 tokenId)
    public
    view
    override(ERC721, ERC721URIStorage)
    returns (string memory)
  {
    return super.tokenURI(tokenId);
  }

  /**
   * @notice Mint a new NFT
   *
   * @param tokenUri The URI of the token being minted
   * @return tokenId The ID of the token minted
   */
  function mint(string memory tokenUri)
    public
    onlyOwner()
    returns (uint256 tokenId)
  {
    _tokenIds.increment();
    tokenId = _tokenIds.current();
    _mint(msg.sender, tokenId);
    _setTokenURI(tokenId, tokenUri);
  }

  /// @dev Allows execution only if the caller is the owner
  modifier onlyOwner() {
    require(
      msg.sender == owner,
      "Only owner can call this function."
    );
    _;
  }
}
