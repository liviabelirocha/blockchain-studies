# Blockchain Studies

- Smart Contracts with Solidity
- Web3 deploy
- Brownie applications

I used in most projects:

- `ganache-cli` to run local blockchains

<hr>

## To create a `mainnet-fork` with brownie

```bash
$ brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=ALCHEMY_HTTP_ADDRESS accounts=10 mnemonic=brownie port=8545
```
