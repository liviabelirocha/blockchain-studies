// SPDX-License-Identifier: MIT

// Smart contract that lets anyone deposit ETH into the contract
// Only the owner of the contract can withdraw the ETH
pragma solidity >=0.6.6 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    // wont allow occasional overflow
    using SafeMathChainlink for uint256;

    // Rinkeby network ETH/USD
    address private EthUsdAddress = 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e;

    mapping(address => uint256) public addressToAmountFunded;
    address public owner;
    address[] public funders;

    constructor() public {
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minimunUsd = 50 * 10 ** 18;
        require(getConversionRate(msg.value) >= minimunUsd, "You need to spend at least 50$!");

        // msg => keyword in every contract transaction
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(EthUsdAddress);
        return priceFeed.version();
    }

    function getPrice() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(EthUsdAddress);
        (,int256 answer,,,) = priceFeed.latestRoundData();
        // ETH/USD rate in 18 digit (wei)
         return uint256(answer * 10000000000);
    }

    // in gwei
    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

     modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        // this -> this contract
        msg.sender.transfer(address(this).balance);

        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        funders = new address[](0);
    }
}