from bananopie import *
#import time

rpc = RPC("https://kaliumapi.appditto.com/api")

print("RPC and utils test")
#check current blockcount
print(rpc.get_block_count()["count"])

#get last 10 transactions of JungleTV
print(rpc.get_account_history("ban_1jung1eb3uomk1gsx7w6w7toqrikxm5pgn5wbsg5fpy96ckpdf6wmiuuzpca", count=10)["history"][0])

#test 'head' for account history
account_history_jtv = rpc.get_account_history("ban_1jung1eb3uomk1gsx7w6w7toqrikxm5pgn5wbsg5fpy96ckpdf6wmiuuzpca", head="2E80DCB9BA76E23337A56CA055B1719C1C43F1F2B7EA2966C2C5140FDA23D865", count=30)
assert account_history_jtv["history"][0]["hash"] == "2E80DCB9BA76E23337A56CA055B1719C1C43F1F2B7EA2966C2C5140FDA23D865"
assert account_history_jtv["history"][1]["hash"] == "F15B1F6E9F03A122FE9C8DC02783CFD47AE86619FD9EF23B415DCE230E62CB1C"
assert len(account_history_jtv["history"]) == 30

#test get blocks info
assert rpc.get_blocks_info(["0A53E2E8ACD2CD2B57EBEB686B3EF5DFB265C3CAC4BDD508B8F076D1BBEE1D1C", "2E80DCB9BA76E23337A56CA055B1719C1C43F1F2B7EA2966C2C5140FDA23D865"])["blocks"]["2E80DCB9BA76E23337A56CA055B1719C1C43F1F2B7EA2966C2C5140FDA23D865"]["contents"]["representative"] == "ban_19potasho7ozny8r1drz3u3hb3r97fw4ndm4hegdsdzzns1c3nobdastcgaa"

#receivable test
assert rpc.get_receivable("ban_1burnbabyburndiscoinferno111111111111111111111111111aj49sw3w", threshold = "97380144580000000000000000000000000000")["blocks"]["26722EF85256481A358A538D6D0EDA1B8B8F337AD4F9CB58C41BBC44949FDA21"] == "97380144586000000000000000000000000000"

#check balance of JungleTV
print(raw_to_whole(int(rpc.get_account_balance("ban_1jung1eb3uomk1gsx7w6w7toqrikxm5pgn5wbsg5fpy96ckpdf6wmiuuzpca")["balance"])))

assert whole_to_raw("492.2") == 49220000000000000000000000000000
assert raw_to_whole(15*(10**BANANO_DECIMALS)) == 15.0
assert raw_to_whole(15.111*(10**BANANO_DECIMALS)) == 15.11
assert raw_to_whole(15.111*(10**BANANO_DECIMALS), precision=3) == 15.111

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
print(my_account.send("ban_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "0.1")["hash"])

#change rep
print("Change test")
print(my_account.change_rep("ban_3catgir1p6b1edo5trp7fdb8gsxx4y5ffshbphj73zzy5hu678rsry7srh8b"))

#change seed index
my_account.index = 1

assert my_account.get_address() == "ban_1rgkz7ipqntii8ic9j411agmtf6do3nxseey3x4jhrqsjcoitj3g9zgi9f53"

print(my_account.receive_all())

print(my_account.send("ban_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "0.0040000501"))

#generate work test
no_work_rpc = RPC("https://public.node.jungletv.live/rpc", legacy=True)

#print(no_work_rpc.get_receivable("ban_1mayorbance1ot1sburnedbananas11111111111111111111111zsqrpxj1", count = 1))

#gen_work

assert gen_work("B7FBEF33567E37E04E772C473CCED4FA9245CC7A4C1BDE8A2576F7384E7919E1") == "0000000000423B3B"

assert verify_work("C6A3732E65800203CE0F32DE710CC110A0CA93C0080F5F0C84A352978DB285F9", "58C5C876832364CC") == True

my_work_account = Wallet(no_work_rpc, seed="3AB019DFCBA0B3763A75B8717EE7900911C7DD4E3B6E31FAE8906EDA71521C98", index=0, try_work=True)

my_work_account.receive_all()

my_work_account.send("ban_3pdripjhteyymwjnaspc5nd96gyxgcdxcskiwwwoqxttnrncrxi974riid94", "0.0145")

#signing test
print("Signing test")

message_signature = my_work_account.sign_message("testing1234")

my_work_public_key = my_work_account.get_public_key()

assert message_signature == "D945708F73E35DA84D3604FF7A9910CD73CE9133B7CB984D0DB50D744BC9C5B46FCBA730DEAA480258BFC1118D6C4635710CF6002C9AFBAADF6BE6CBD526880B"

assert verify_message(my_work_public_key, message_signature, "testing1234")

assert not verify_message(my_work_public_key, message_signature, "testing123")

assert not verify_message(my_work_public_key, message_signature, "weee")

message_signature_dummy_block = my_work_account.sign_message_dummy_block("testing1234")

assert message_signature_dummy_block == "734D535A9BA1ADF53BC47036FDFE6ADFFFE2D28C7DDCA6C05E76CBB8F70CA33E6B23824C91D780E8C23849ADD8566EC258629C8261E7EC438E75B218860D0002"

assert verify_message_dummy_block(my_work_public_key, message_signature_dummy_block, "testing1234")

assert not verify_message_dummy_block(my_work_public_key, message_signature_dummy_block, "testing123")

assert not verify_message_dummy_block(my_work_public_key, message_signature_dummy_block, "weee")

#Send all and previous test
print("send all and previous test")

my_account_tres = Wallet(rpc, seed="3AB019DFCBA0B3763A75B8717EE7900911C7DD4E3B6E31FAE8906EDA71521C98", index=2)

receive_tres_hash = my_account_tres.receive_specific("E2F215CF902363A7F41D36D571DB5E0BF26AE82C86C6CA6739A9C9BD80666E50")["hash"]

send_1_hash = my_account_tres.send("ban_1jtn1jnkgdqesy9idaz3y398y3oqqxyxzueitot8ykr1a9onawd35aq3whf9", 1, previous=receive_tres_hash)["hash"]

try:
  my_account_tres.send("ban_1jtn1jnkgdqesy9idaz3y398y3oqqxyxzueitot8ykr1a9onawd35aq3whf9", 1, previous=receive_tres_hash)
  print("this shouldn't print, previous send should've failed")
except Exception as e:
  pass

my_account_tres.send_all("ban_1jtn1jnkgdqesy9idaz3y398y3oqqxyxzueitot8ykr1a9onawd35aq3whf9", previous=send_1_hash)
