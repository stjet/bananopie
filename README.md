# Bananopie

Bananopie is a python library for the Banano cryptocurrency. It aims to be the python equivalent of Banano.js, and not just a RPC wrapper (Sending, receiving, changing rep functions are very high level).

## Installation

`pip install bananopie`

Bananopie is on [pypi](https://pypi.org/project/bananopie/).

## Notes
- There is an outdated fork of Bananopie for Nano, also made by me, called [nanohakase](https://pypi.org/project/nanohakase/). It should suit most of your needs, but if you need new Bananopie features, fork Bananopie, change the work difficulty to `FFFFFFF800000000`, decimals to `31`, and you should be good to go.
- When running on Replit (ew), installing Bananopie may fail if you do not have `gcc` installed (nix package: `libgccjit`).

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
print(my_account.send("ban_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "1")["hash"])

#receive funds
my_account.receive_all()

#change rep
my_account.change_rep("ban_3catgir1p6b1edo5trp7fdb8gsxx4y5ffshbphj73zzy5hu678rsry7srh8b")

#change seed index
my_account.index = 2
```

Bananopie can also generate work, albeit slowly. This is useful when using node that don't support generating work. Also, the `legacy` parameter can be passed to the RPC class when the RPC supports the deprecated `pending` RPC call instead of the newer `receivable` call.
```py
from bananopie import RPC, Wallet

no_work_rpc = RPC("https://public.node.jungletv.live/rpc", legacy=True)

my_work_account = Wallet(no_work_rpc, seed="seed here", index=0, try_work=True)

#will generate work locally!
my_work_account.send("ban_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "0.0042")
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
- `legacy` (*bool*, Default: False): If `True`, will use 'pending' instead of 'receivable'

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
- `blocks` (*list[str]*): List of block hashes to get information on

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#blocks)

### get_blocks_info (Function)
Get blocks, with more detailed information.

**Parameters**
- `blocks` (*list[str]*): List of block hashes to get information on

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
- `head` (*str* or *None*, Default: None): Block hash to start from, defaults to latest block hash if omitted
- `account_filter` (*list[str]* or *None*, Default: None): List of addresses to only show sends/receives from. Please note that some public nodes will ignore this parameter

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
- `account` (*list[str]*): List of addresses

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
- `threshold` (*int* or *None*, Default: None): Optional parameter to filter out any receivable transactions with value below the threshold (in raw)

**Returns:**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#receivable)

## Wallet (class)

**Parameters:**
- `rpc` (*RPC*): A RPC class
- `seed` (*str* or *None*, Default: None): 64 character hex seed, if `None`, will generate a seed by itself. Private keys are derived from the seed.
- `index` (*int*, Default: 0): Optional parameter that is the index of the seed. Any number from 0 to 4294967295. Each index of the seed is a different private key, and so different address.
- `try_work` (*bool*, Default: False): If `True`, will try to generate work locally instead of asking node for work (and no work provided). Good to use if node does not support generating own work.

Sample:
```py
my_account = Wallet(RPC("https://kaliumapi.appditto.com/api"), "seed here", 0)
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
- `work` (*str* or *bool* or *function*, Default: False): Leave it as `False` to ask node to generate work (passes `do_work`). Put in a work string if work generated locally, if it is a function, the work will be the function called with the block hash as a parameter (keep in mind you can set the class' `try_work` to `True` to use the built-in `gen_work` function)
- `previous` (*str* or *None*, Default: None): Previous block hash. Otherwise, address' frontier block hash used

Sample:
```py
my_account = Wallet(RPC("https://kaliumapi.appditto.com/api"), "seed here", 0)
my_account.send("ban_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "1")
```

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### send_all (Function)
High level function to send all Banano

**Parameters**
- `to` (*str*): Address to send to
- `work` (*str* or *bool* or *function*, Default: False): Leave it as `False` to ask node to generate work (passes `do_work`). Put in a work string if work generated locally, if it is a function, the work will be the function called with the block hash as a parameter (keep in mind you can set the class' `try_work` to `True` to use the built-in `gen_work` function)
- `previous` (*str* or *None*, Default: None): Previous block hash. Otherwise, address' frontier block hash used

Sample:
```py
my_account = Wallet(RPC("https://kaliumapi.appditto.com/api"), "seed here", 0)
my_account.send_all("ban_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94")
```

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### receive_specific (Function)
Receive a specific block

**Parameters**
- `hash` (*str*): Block hash to receive
- `work` (*str* or *bool* or *function*, Default: False): Leave it as `False` to ask node to generate work (passes `do_work`). Put in a work string if work generated locally, if it is a function, the work will be the function called with the block hash as a parameter (keep in mind you can set the class' `try_work` to `True` to use the built-in `gen_work` function)
- `previous` (*str* or *None*, Default: None): Previous block hash. Otherwise, address' frontier block hash used

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### receive_all (Function)
Receive all (technically, 20) receivable transactions

**Parameters**
- `count` (*int*, Default: 20): Optional parameter to specify max amount of receivable transactions to receive
- `threshold` (*int* or *None*, Default: None): Optional parameter to not receive any receivable transactions with value below the threshold (in whole, not raw)

Sample:
```py
my_account = Wallet(RPC("https://kaliumapi.appditto.com/api"), "seed here", 0)
my_account.receive_all()
```

**Returns**
- A list of block hashes that were received (See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process))

### change_rep (Function)
Change account representative

**Parameters**
- `new_representative` (*str*): Representative Banano address to change to
- `work` (*str* or *bool* or *function*, Default: False): Leave it as `False` to ask node to generate work (passes `do_work`). Put in a work string if work generated locally, if it is a function, the work will be the function called with the block hash as a parameter (keep in mind you can set the class' `try_work` to `True` to use the built-in `gen_work` function)
- `previous` (*str* or *None*, Default: None): Previous block hash. Otherwise, address' frontier block hash used

Sample:
```py
my_account = Wallet(RPC("https://kaliumapi.appditto.com/api"), "seed here", 0)
my_account.change_rep("ban_3catgir1p6b1edo5trp7fdb8gsxx4y5ffshbphj73zzy5hu678rsry7srh8b")
```

**Returns**
See [Nano RPC Docs](https://docs.nano.org/commands/rpc-protocol/#process)

### sign_message (Function)
Sign utf-8 message with private key at current index of current seed

**Parameters**
- `message` (*str*): utf-8 message to sign

**Returns**
*str*, Hex signature

### sign_message_dummy_block (Function)
Sign utf-8 message as a dummy block (making sure ledger devices can also sign) with private key at current index of current seed

**Parameters**
- `message` (*str*): utf-8 message to sign

**Returns**
*str*, Hex signature

### get_public_key (Function)
Get public key at current index of current seed

**Parameters**
None

**Returns**
*str*, Hex public key

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

### get_receivable_whole_threshold (Function)
Double wrapped function to get receivable blocks (see `RPC`'s `get_receivable`), except `threshold` parameter is in whole Banano, not raw

### get_representative (Function)
Double wrapped function to get representative of self (see `RPC`'s `get_account_representative`)

### get_account_info (Function)
Double wrapped function to get account info of self (see `RPC`'s `get_account_info`)

### get_account_history (Function)
Double wrapped function to get account info of self (see `RPC`'s `get_account_history`)

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
- `BANANO_WORK` (*str*): Hex string of Banano's work threshold/minimum

**Methods**

`encode_base32`, `decode_base32`, `bytes_to_hex`, `hex_to_bytes`, `utf8_to_bytes`, `random_bytes`, `get_private_key_from_seed`, `get_public_key_from_private_key`, `get_address_from_public_key`, `get_public_key_from_address`, `hash_block`, `sign`, `sign_message_dummy_block`, `gen_dummy_block_hash` are internal use Functions that are currently undocumented. Look at `/bananopie/util.py` to see what they do.

### verify_message (Function)
Verifies whether signed message is real

**Parameters**
- `public_key` (*str*): Hex public key
- `signature` (*str*): Hex signature
- `claimed_message` (*str*): utf-8 message that was allegedly signed

**Returns**
*bool*, `True` if message verified, `False` if message not verified

### verify_message_dummy_block (Function)
Verifies whether signed message (with dummy block) is real

**Parameters**
- `public_key` (*str*): Hex public key
- `signature` (*str*): Hex signature
- `claimed_message` (*str*): utf-8 message (with dummy block) that was allegedly signed

**Returns**
*bool*, `True` if message (with dummy block) verified, `False` if message (with dummy block) not verified

### whole_to_raw (Function)
Converts whole Banano to raw Banano

**Parameters**
- `whole` (*str*): Whole amount of Banano

**Returns**
*int*, that is raw amount of Banano

### raw_to_whole (Function)
Converts raw Banano to whole Banano (Cuts off at 2 decimal places by default)

**Parameters**
- `raw` (*int*): Raw amount of Banano
- `precision` (*int*, Default: 2): Decimal places to cut off at

**Returns**
*int*, that is whole amount of Banano

### raw_to_whole_no_round (Function)
Converts raw Banano to whole Banano, without rounding

**Parameters**
- `raw` (*int*): Raw amount of Banano

**Returns**
*str*, that is unrounded whole amount of Banano

### gen_work_random (Function)
Generate work given block's previous hash (or if opening block, account public key), and threshold. Generates work using psuedorandom generator.

**Parameters**
- `hash` (*str*): Hex previous hash of block / account public key
- `threshold` (*str*): Hex minimum work threshold

**Returns**
*str*, that is hex of work

### gen_work_deterministic (Function)
Generate work given block's previous hash (or if opening block, account public key), and threshold. Generates work deterministically.

**Parameters**
- `hash` (*str*): Hex previous hash of block / account public key
- `threshold` (*str*): Hex minimum work threshold

**Returns**
*str*, that is hex of work

### gen_work (Function)
Generate work given block's previous hash (or if opening block, account public key). Basically a wrapper for `gen_work_deterministic` with threshold being the hardcoded Banano default.

**Parameters**
- `hash` (*str*): Hex previous hash of block / account public key

**Returns**
*str*, that is hex of work

### verify_work (Function)
Verify whether work is valid or not, given previous hash of block (or if opening block, account public key).

**Parameters**
- `hash` (*str*): Hex previous hash of block / account public key
- `work` (*str*): Hex of work

**Returns**
*bool*, whether the work is valid or not
