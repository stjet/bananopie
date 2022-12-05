# Bananopie

Bananopie is a python library for the Banano cryptocurrency. It aims to be the python equivalent of Banano.js, and not just a RPC wrapper (Sending, receiving, changing rep functions are very high level).

## Installation

`pip install bananopie`

Bananopie is on [pypi](https://pypi.org/project/bananopie/).

# Quick Start

First, start with a `RPC` class, for read only 
```py
from bananopie import *
rpc = RPC("https://kaliumapi.appditto.com/api")

#check current blockcount
print(rpc.get_block_count()["count"])

#get last 10 transactions of JungleTV
print(rpc.get_account_history("ban_1jung1eb3uomk1gsx7w6w7toqrikxm5pgn5wbsg5fpy96ckpdf6wmiuuzpca", count=10)["history"])

#check balance of JungleTV
print(raw_to_whole(int(rpc.get_account_balance("ban_1jung1eb3uomk1gsx7w6w7toqrikxm5pgn5wbsg5fpy96ckpdf6wmiuuzpca")["balance"])))
```

For sending/receiving transactions, use a `Wallet`.
```py
from bananopie import RPC, Wallet
rpc = RPC("https://kaliumapi.appditto.com/api")

my_account = Wallet(rpc, seed="seed here", index=0)

#or generate a new one
my_new_account = Wallet(rpc, index=0)

print(my_new_account.seed)

#get address of self
print(my_account.get_address())

#get balance of self
print(my_account.get_balance())

#send 1 banano to the faucet development fund
print(my_account.send("ban_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "1"))

#receive funds
my_account.receive_all()

#change rep
my_account.change_rep("ban_3catgir1p6b1edo5trp7fdb8gsxx4y5ffshbphj73zzy5hu678rsry7srh8b")

#change seed index
my_account.index = 2
```

Utility functions are also provided.
```py
import bananopie

#whole to raw banano
print(bananopie.whole_to_raw("492.2"))

#raw to whole banano
print(bananopie.raw_to_whole(1900000000000000000000000000))
```

# Documentation

Also see the [Nano RPC docs](https://docs.nano.org/commands/rpc-protocol) for information on what rpc call wrapper functions return.

## RPC (Class)
**Parameters:**
- `rpc_url` (*str*): IP or URL of node
- `auth` (*str* or *bool*, Default: False): Optional HTTP Authorization header

Sample:
```py
rpc = RPC("https://kaliumapi.appditto.com/api")
```

**Properties:**
- `rpc_url` (*str*): IP or URL of node
- `auth` (*str* or *bool*): Optional HTTP Authorization header

**Methods:**

### call (Function)
RPC call. Intended for internal use, but useful for RPC calls that aren't directly implemented.

**Parameters:**
- `payload` (*dictionary*): Payload to send to node

Sample:
```py
rpc.call({"action": "block_count"})
```

**Returns:**
Response of RPC call (JSON dictionary)

### get_block_count (Function)
Get network block count.

**Parameters**
None

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#block_count)


### get_block_info (Function)
Get block info for hash.

**Parameters**
- `block` (*st*): Block hash

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#block_info)

### get_blocks (Function)
Get blocks.

**Parameters**
- `blocks` (*str list*): List of block hashes to get information on

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#blocks)

### get_blocks_info (Function)
Get blocks, with more detailed information.

**Parameters**
- `blocks` (*str list*): List of block hashes to get information on

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#blocks_info)

### get_representatives (Function)
Get list of network representatives and their weight

**Parameters**
None

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#representatives)

### get_representatives_online (Function)
Get list of network representatives that have recently voted

**Parameters**
None

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#representatives_online)

### get_account_history (Function)
Get account history (confirmed and received transaction list)

**Parameters**
- `account` (*str*): Address of account
- `count` (*int*, Default: -1): Optional parameter to specify amount of transactions to return. `-1` means all, or at least as much as the node will allow

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_history)

### get_account_info (Function)
Get account information, like height, frontier, balance, etc

**Parameters**
- `account` (*str*): Address of account

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_info)

### get_account_balance (Function)
Get account balance

**Parameters**
- `account` (*str*): Address of account

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_balance)

### get_account_representative (Function)
Get account representative

**Parameters**
- `account` (*str*): Address of account

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_representative)

### get_accounts_representatives (Function)
Get representatives of accounts

**Parameters**
- `account` (*str list*): List of addresses

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_representatives)

### get_account_weight (Function)
Get delegated weight of representative

**Parameters**
- `account` (*str*): Address of representative

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#account_weight)

### get_receivable (Function)
Get receivable transactions for account

**Parameters**
- `account` (*str*): Address of representative
- `count` (*int*, Default: 20): Optional parameter to specify max amount of receivable transactions to return
- `thereshold` (*int or bool*, Default: False): Optional parameter to filter out any receivable transactions with value less than the thereshold

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#receivable)

## Wallet (class)

**Parameters:**
- `rpc` (*RPC*): A RPC class
- `seed` (*str* or *bool*, Default: False): 64 character hex seed, if `False`, will generate a seed by itself. Private keys are derived from the seed.
- `index` (*int*, Default: 0): Optional parameter that is the index of the seed. Any number from 0 to 4294967295. Each index of the seed is a different private key, and so different address.

Sample:
```py
my_wallet = Wallet(RPC("https://kaliumapi.appditto.com/api"), "seed here", 0)
```

**Properties:**
- `rpc_url` (*str*): IP or URL of node
- `seed` (*str*): Banano seed (64 character hex string)
- `index` (*int*): Seed index. Change this property to change the wallet seed index.

**Methods**

### send_process (Function)
Internal use function to send a `process` RPC call

**Parameters**
- `block` (*dictionary*): block content
- `subtype` (*str*): Send, receive, or change

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### send (Function)
High level function to send Banano

**Parameters**
- `to` (*str*): Address to send to
- `amount` (*str*): Amount of Banano to send (in whole, not raw)
- `work` (*str* or *bool*, Default: False): Leave it as False to ask node to generate work (passes `do_work`). Put in a work string if work generated locally

Sample:
```py
my_wallet = Wallet(RPC("https://kaliumapi.appditto.com/api"), "seed here", 0)
my_account.send("ban_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "1")
```

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### receive_specific (Function)
Receive a specific block

**Parameters**
- `hash` (*str*): Block hash to receive
- `work` (*str* or *bool*, Default: False): Leave it as False to ask node to generate work (passes `do_work`). Put in a work string if work generated locally

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### receive_all (Function)
Receive all (technically, 20) receivable transactions

**Parameters**
None

Sample:
```py
my_wallet = Wallet(RPC("https://kaliumapi.appditto.com/api"), "seed here", 0)
my_account.receive_all()
```

**Returns**
Nothing

### change_rep (Function)
Change account representative

**Parameters**
- `new_representative` (*str*): Representative Banano address to change to
- `work` (*str* or *bool*, Default: False): Leave it as False to ask node to generate work (passes `do_work`). Put in a work string if work generated locally

Sample:
```py
my_wallet = Wallet(RPC("https://kaliumapi.appditto.com/api"), "seed here", 0)
my_account.change_rep("ban_3catgir1p6b1edo5trp7fdb8gsxx4y5ffshbphj73zzy5hu678rsry7srh8b")
```

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### get_address (Function)
Get address at current index of current seed

**Parameters**
None

**Returns**
*str*, Banano address

### get_balance (Function)
Double wrapped function to get balance of self (see `RPC`'s `get_account_balance`)

### get_receivable (Function)
Double wrapped function to get receivable blocks (see `RPC`'s `get_receivable`)

### get_representative (Function)
Double wrapped function to get representative of self (see `RPC`'s `get_account_representative`)

### get_account_info (Function)
Double wrapped function to get account info of self (see `RPC`'s `get_account_info`)

### generate_seed (static Function)
Generate a random seed using `os.urandom`

**Parameters**
None

Sample:
```py
print(Wallet.generate_seed())
```

**Returns**
64 character hex seed

## Util

**Properties**
- `BANANO_DECIMALS` (*int*): Amount of decimals that Banano has (29)
- `PREAMBLE` (*str*): Hex string to prepend when signing

**Methods**

`encode_base32`, `decode_base32`, `bytes_to_hex`, `hex_to_bytes`, `random_bytes`, `get_private_key_from_seed`, `get_public_key_from_private_key`, `get_address_from_public_key`, `get_public_key_from_address`, `hash_block`, `sign` are internal use Functions that are currently undocumented. Look at `/bananopie/util.py` to see what they do.

### whole_to_raw (Function)
Converts whole Banano to raw Banano

**Parameters**
- `whole` (*str*): Whole amount of Banano

**Returns**
*int*, that is raw amount of Banano

### raw_to_whole (Function)
Converts raw Banano to whole Banano (Cuts off at 2 decimal places)

**Parameters**
- `raw` (*int*): Raw amount of Banano

**Returns**
*int*, that is whole amount of Banano
