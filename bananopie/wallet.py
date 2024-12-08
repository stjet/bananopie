from .rpc import RPC
from .util import *

#todo: request work with work_generate
class Wallet:
  def __init__(self, rpc: RPC, seed = None, index: int = 0, try_work = False):
    self.rpc = rpc
    #if seed is False, automatically generate new seed
    if not seed:
      seed = self.generate_seed()
    self.seed = seed
    self.index = index
    self.try_work = try_work
  @staticmethod
  def generate_seed():
    return bytes_to_hex(random_bytes(32))
  def get_public_key(self) -> str:
    return get_public_key_from_private_key(get_private_key_from_seed(self.seed, self.index))
  def get_address(self) -> str:
    return get_address_from_public_key(self.get_public_key())
  def send_process(self, block, subtype: str):
    payload = {
      "action": "process",
      "subtype": subtype,
      "json_block": "true",
      "block": block
    }
    if "work" not in block:
      if self.try_work:
        #if opening block, there is no previous, so use public key as hash instead
        if block["previous"] == "0000000000000000000000000000000000000000000000000000000000000000":
          block["work"] = gen_work(self.get_public_key())
        else:
          block["work"] = gen_work(block["previous"])
      else:
        payload["do_work"] = True
    return self.rpc.call(payload)
  #actions
  def send(self, to: str, amount: str, work = False, previous = None):
    amount = whole_to_raw(amount)
    address_sender = self.get_address()
    private_key_sender = get_private_key_from_seed(self.seed, self.index)
    #public_key_sender = get_public_key_from_private_key(get_private_key_from_seed(self.seed, self.index))
    public_key_receiver = get_public_key_from_address(to)
    info = self.get_account_info()
    if not previous:
      previous = info["frontier"]
    representative = info["representative"]
    before_balance = info["balance"]
    #height not actually needed
    new_balance = int(int(before_balance)-amount)
    if new_balance < 0:
      raise ValueError(f"Insufficient funds to send. Cannot send more than balance (before balance {str(before_balance)} less than send amount {str(amount)})")
    block = {
      "type": "state",
      "account": address_sender,
      "previous": previous,
      "representative": representative,
      "balance": str(new_balance),
      #link in this case is public key of account to send to
      "link": public_key_receiver,
      "link_as_account": to
    }
    block_hash = hash_block(block)
    signature = sign(private_key_sender, block_hash)
    block["signature"] = signature
    if work:
      if callable(work):
        work = work(block_hash)
      block["work"] = work
    return self.send_process(block, "send")
  def send_all(self, to: str, work = False, previous = None):
    address_sender = self.get_address()
    private_key_sender = get_private_key_from_seed(self.seed, self.index)
    #public_key_sender = get_public_key_from_private_key(get_private_key_from_seed(self.seed, self.index))
    public_key_receiver = get_public_key_from_address(to)
    info = self.get_account_info()
    if not previous:
      previous = info["frontier"]
    representative = info["representative"]
    #height not actually needed
    block = {
      "type": "state",
      "account": address_sender,
      "previous": previous,
      "representative": representative,
      "balance": "0",
      #link in this case is public key of account to send to
      "link": public_key_receiver,
      "link_as_account": to
    }
    block_hash = hash_block(block)
    signature = sign(private_key_sender, block_hash)
    block["signature"] = signature
    if work:
      if callable(work):
        work = work(block_hash)
      block["work"] = work
    return self.send_process(block, "send")
  def receive_specific(self, hash: str, work = False, previous = None):
    #no need to check as opened, I think?
    #get block info of receiving
    block_info = self.rpc.get_block_info(hash)
    amount = int(block_info["amount"])
    address_sender = self.get_address()
    private_key_receiver = get_private_key_from_seed(self.seed, self.index)
    #public_key_sender = get_public_key_from_private_key(get_private_key_from_seed(self.seed, self.index))
    #public_key_sender = get_public_key_from_address(block_info["block_account"])
    #these are the defaults, if the account is unopened
    before_balance = 0
    representative = address_sender
    if not previous:
      try:
        #if account is opened
        info = self.get_account_info()
        previous = info["frontier"]
        representative = info["representative"]
        before_balance = info["balance"]
      except Exception as e:
        #probably, unopened account
        previous = "0000000000000000000000000000000000000000000000000000000000000000"
    #height not actually needed
    block = {
      "type": "state",
      "account": address_sender,
      "previous": previous,
      "representative": representative,
      "balance": str(int(before_balance)+amount),
      #link in this case is hash of send
      "link": hash
    }
    block_hash = hash_block(block)
    signature = sign(private_key_receiver, block_hash)
    block["signature"] = signature
    if work:
      if callable(work):
        work = work(block_hash)
      block["work"] = work
    return self.send_process(block, "receive")
  def receive_all(self, count=20, threshold=None):
    responses = []
    receivable_blocks = self.get_receivable_whole_threshold(count=count, threshold=threshold)["blocks"]
    for block_hash in receivable_blocks:
      #receive them
      responses.append(self.receive_specific(block_hash))
    return responses
  def change_rep(self, new_representative, work = False, previous = None):
    address_self = self.get_address()
    private_key_self = get_private_key_from_seed(self.seed, self.index)
    #public_key_sender = get_public_key_from_private_key(get_private_key_from_seed(self.seed, self.index))
    #account must be opened to do a change rep
    info = self.get_account_info()
    if not previous:
      previous = info["frontier"]
    before_balance = info["balance"]
    block = {
      "type": "state",
      "account": address_self,
      "previous": previous,
      "representative": new_representative,
      "balance": before_balance,
      #link in this case is 0
      "link": "0000000000000000000000000000000000000000000000000000000000000000"
    }
    block_hash = hash_block(block)
    signature = sign(private_key_self, block_hash)
    block["signature"] = signature
    if work:
      if callable(work):
        work = work(block_hash)
      block["work"] = work
    return self.send_process(block, "change")
  def sign_message(self, message: str) -> str:
    private_key_self = get_private_key_from_seed(self.seed, self.index)
    return sign_message(private_key_self, message)
  def sign_message_dummy_block(self, message: str) -> str:
    private_key_self = get_private_key_from_seed(self.seed, self.index)
    return sign_message_dummy_block(private_key_self, message)
  #double wrapped
  def get_balance(self):
    return self.rpc.get_account_balance(self.get_address())
  def get_receivable(self, count: int = 20, threshold = None):
    return self.rpc.get_receivable(self.get_address(), count=count, threshold=threshold)
  def get_receivable_whole_threshold(self, count: int = 20, threshold = None):
    if threshold == None:
      return self.rpc.get_receivable(self.get_address(), count=count)
    else:
      return self.rpc.get_receivable(self.get_address(), count=count, threshold=whole_to_raw(str(threshold)))
  def get_representative(self):
    return self.rpc.get_account_representative(self.get_address())
  def get_account_info(self):
    return self.rpc.get_account_info(self.get_address())
  def get_account_history(self, count: int = -1, head: str = None, account_filter = None): #account_filter: list[str] = None
    return self.rpc.get_account_history(self.get_address(), count=count, head=head, account_filter=account_filter)
