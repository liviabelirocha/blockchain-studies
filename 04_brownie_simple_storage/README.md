# Brownie Simple Storage

### Install Brownie

```bash
$ python3 -m pip install --user pipx
$ python3 -m pipx ensurepath
# restart your terminal
$ pipx install eth-brownie
```
Or, if that doesn't work, via pip
```bash
$ pip install eth-brownie
```

<hr/>

You need ganache-cli installed in order to run a script locally.

```bash
$ yarn global add ganache-cli
# or
$ npm install -g ganache-cli
```

You might need to add that to your environment variables.

### Create Brownie Account

```bash
$ brownie accounts new account_name
```