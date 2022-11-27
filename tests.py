from bananopie import *

#todo: change tests so they use ` ]`

rpc = RPC("https://kaliumapi.appditto.com/api")

print("RPC and utils test")
#check current blockcount
print(rpc.get_block_count()["count"])

#get last 10 transactions of JungleTV
print(rpc.get_account_history("ban_1jung1eb3uomk1gsx7w6w7toqrikxm5pgn5wbsg5fpy96ckpdf6wmiuuzpca", count=10)["history"][0])

#check balance of JungleTV
print(raw_to_whole(int(rpc.get_account_balance("ban_1jung1eb3uomk1gsx7w6w7toqrikxm5pgn5wbsg5fpy96ckpdf6wmiuuzpca")["balance"])))

assert whole_to_raw(492.2) == 4.922e+31
assert raw_to_whole(15*(10**BANANO_DECIMALS)) == 15.0

#if someone drains the funds in this test seed I will be very upset >:(
print("Wallets test")
my_account = Wallet(rpc, seed="3AB019DFCBA0B3763A75B8717EE7900911C7DD4E3B6E31FAE8906EDA71521C98", index=0)

#or generate a new one
my_new_account = Wallet(rpc, index=0)

print(my_new_account.seed)

#get address of self
assert my_account.get_address() == "ban_1jtn1jnkgdqesy9idaz3y398y3oqqxyxzueitot8ykr1a9onawd35aq3whf9"

#get balance of self
print(my_account.get_balance())

#receive all transactions
print("Receive test")
print(my_account.receive_all())

#send 1 banano to the faucet development fund
print("Send test")
print(my_account.send("ban_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", 1))

#receive funds
print("Change test")
print(my_account.change_rep("ban_3catgir1p6b1edo5trp7fdb8gsxx4y5ffshbphj73zzy5hu678rsry7srh8b"))

#change rep

#change seed index
my_account.index = 2
