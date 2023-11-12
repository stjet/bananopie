import os, math, random
from hashlib import blake2b
import ed25519_blake2b
from decimal import Decimal, getcontext

BANANO_DECIMALS = 29
#banano supply is 1.000.000.000+, so add 10 decimals
getcontext().prec = BANANO_DECIMALS+10
PREAMBLE = "0000000000000000000000000000000000000000000000000000000000000006"
#FFFFFFF000000000 FFFFFE0000000000
BANANO_WORK = "FFFFFE0000000000"

MESSAGE_PREAMBLE = "62616E616E6F6D73672D" #bananomsg-

#this function translated to python from https://nanoo.tools/js/termhn_nano-base32_2018-03-06.js
def encode_base32(bytes) -> str:
  alphabet = '13456789abcdefghijkmnopqrstuwxyz'
  length = len(bytes)
  leftover = (length * 8) % 5
  offset = 0
  if leftover == 0:
    offset = 0
  else:
    offset = 5 - leftover
  value = 0
  output = ''
  bits = 0
  for i in range(length):
    value = (value << 8) | bytes[i]
    bits += 8
    while (bits >= 5):
      output += alphabet[(value >> (bits + offset - 5)) & 31]
      bits -= 5
  if bits > 0:
    output += alphabet[(value << (5 - (bits + offset))) & 31]
  return output

def decode_base32(base32: str) -> bytes:
  alphabet = '13456789abcdefghijkmnopqrstuwxyz'
  length = len(base32)
  leftover = (length * 5) % 8
  offset = 0
  if leftover == 0:
    offset = 0
  else:
    offset = 8 - leftover
  bits = 0
  value = 0
  index = 0
  output = bytearray(math.ceil(length * 5 / 8))
  for i in range(length):
    value = (value << 5) | alphabet.index(base32[i])
    bits += 5
    if bits >= 8:
      output[index] = (value >> (bits + offset - 8)) & 255
      index += 1
      bits -= 8
  if bits > 0:
    output[index] = (value << (bits + offset - 8)) & 255
    index += 1
  if leftover != 0:
    output = output[1::]
  return bytes(output)

def bytes_to_hex(bytes: bytes) -> str:
  return bytes.hex().upper()

def hex_to_bytes(hex: str) -> bytes:
  #seems to return big endian
  return bytes.fromhex(hex)

def utf8_to_bytes(message: str):
  return message.encode()

#bytes_num should be 32, usually
def random_bytes(bytes_num: int):
  return os.urandom(bytes_num)

def get_private_key_from_seed(seed: str, seed_index: int) -> str:
  #https://docs.nano.org/glossary/#wallet
  #seed_index is 32 bit (4 bytes)
  #use hashlib blake2b
  seed_index = seed_index.to_bytes(4, "big")
  seed = hex_to_bytes(seed)
  blake_obj = blake2b(digest_size=32)
  blake_obj.update(seed)
  blake_obj.update(seed_index)
  return blake_obj.hexdigest()

def get_public_key_from_private_key(private_key: str) -> str:
  return bytes_to_hex(ed25519_blake2b.SigningKey(hex_to_bytes(private_key)).get_verifying_key().to_bytes())

def get_address_from_public_key(public_key: str) -> str:
  #nanoo.tools
  public_key = hex_to_bytes(public_key)
  first = encode_base32(public_key)
  blake_obj = blake2b(digest_size=5)
  blake_obj.update(public_key)
  #reverse
  checksum = encode_base32(blake_obj.digest()[::-1])
  #base 32 public key, add checksum
  return "ban_"+first+checksum

def get_public_key_from_address(address: str) -> str:
  #ignore checksum for now. todo: don't ignore
  address = address.replace("ban_", "")
  return bytes_to_hex(decode_base32(address[0:52]))

def hash_block(block) -> str:
  blake_obj = blake2b(digest_size=32)
  blake_obj.update(hex_to_bytes(PREAMBLE))
  blake_obj.update(hex_to_bytes(get_public_key_from_address(block["account"])))
  blake_obj.update(hex_to_bytes(block["previous"]))
  blake_obj.update(hex_to_bytes(get_public_key_from_address(block["representative"])))
  padded_balance = hex(int(block["balance"])).replace("0x","")
  while len(padded_balance) < 32:
    padded_balance = '0' + padded_balance
  blake_obj.update(hex_to_bytes(padded_balance))
  blake_obj.update(hex_to_bytes(block["link"]))
  #return hash
  return bytes_to_hex(blake_obj.digest())

def sign(private_key: str, hash: str) -> str:
  #ed25519_blake2b verify
  signing_key = ed25519_blake2b.SigningKey(hex_to_bytes(private_key))
  signature = bytes_to_hex(signing_key.sign(hex_to_bytes(hash)))
  return signature

def sign_message(private_key: str, message: str) -> str:
  signing_key = ed25519_blake2b.SigningKey(hex_to_bytes(private_key))
  signature = bytes_to_hex(signing_key.sign(utf8_to_bytes(message)))
  return signature

def verify_message(public_key: str, signature: str, claimed_message: str) -> bool:
  verifying_key = ed25519_blake2b.VerifyingKey(hex_to_bytes(public_key))
  try:
    verifying_key.verify(hex_to_bytes(signature), utf8_to_bytes(claimed_message))
    return True
  except:
    return False

def gen_dummy_block_hash(public_key: str, message: str) -> bytes:
  dummy_16 = hex_to_bytes("00000000000000000000000000000000")
  dummy_32 = hex_to_bytes("0000000000000000000000000000000000000000000000000000000000000000")
  blake_obj = blake2b(digest_size=32)
  blake_obj.update(hex_to_bytes(PREAMBLE))
  blake_obj.update(hex_to_bytes(public_key))
  blake_obj.update(dummy_32)
  #we are putting the hashed message into the representative field
  blake_obj_message = blake2b(digest_size=32)
  blake_obj_message.update(hex_to_bytes(MESSAGE_PREAMBLE))
  blake_obj_message.update(utf8_to_bytes(message))
  blake_obj.update(blake_obj_message.digest())
  blake_obj.update(dummy_16)
  blake_obj.update(dummy_32)
  #return hash
  return blake_obj.digest()
  
def sign_message_dummy_block(private_key: str, message: str) -> str:
  signing_key = ed25519_blake2b.SigningKey(hex_to_bytes(private_key))
  dummy_block_hash = gen_dummy_block_hash(get_public_key_from_private_key(private_key), message)
  #assert bytes_to_hex(dummy_block_hash) == "041E2C42234229B51F21AD6824D557DBAE02A180C9050E6E82021E22D517C6FD"
  signature = bytes_to_hex(signing_key.sign(dummy_block_hash))
  return signature

def verify_message_dummy_block(public_key: str, signature: str, claimed_message: str) -> bool:
  dummy_block_hash = gen_dummy_block_hash(public_key, claimed_message)
  verifying_key = ed25519_blake2b.VerifyingKey(hex_to_bytes(public_key))
  try:
    verifying_key.verify(hex_to_bytes(signature), dummy_block_hash)
    return True
  except:
    return False

def whole_to_raw(whole: str) -> int:
  return int(Decimal(whole)*(10**BANANO_DECIMALS))

def raw_to_whole(raw: int, precision: int = 2):
  return math.floor((raw*(10**precision))/(10**BANANO_DECIMALS))/(10**precision)

def raw_to_whole_no_round(raw: int) -> str:
  return str(Decimal(raw)/Decimal(10**BANANO_DECIMALS))
    
#the hash should be the block previous hash, or if first transaction, the account public key
def gen_work_random(hash: str, threshold: str) -> str:
  #generate work with random.randbytes()
  while True:
    #work is 64 bit (8 byte) nonce
    #only generate 3 random bytes, first 5 are 0s. I see kalium do that I think, so I dunno if its more efficient but I copied that
    #nonce = hex_to_bytes("0000000000"+bytes_to_hex(random.randbytes(3)))
    nonce = random.randbytes(8)
    #when blake2b hashed with the hash, should be larger than the threshold
    blake_obj = blake2b(digest_size=8)
    blake_obj.update(nonce)
    blake_obj.update(hex_to_bytes(hash))
    #since hex_to_bytes returns big endian, for BANANO_WORK, after we convert to hex, we convert to bytes with big endian
    if int.from_bytes(blake_obj.digest(), byteorder="little") > int.from_bytes(hex_to_bytes(threshold), byteorder="big"):
      #return as big endian
      return bytes_to_hex(bytearray.fromhex(bytes_to_hex(nonce))[::-1])

def gen_work_deterministic(hash: str, threshold: str) -> str:
  #generate work deterministically by incrementing by 1
  nonce = 0
  while True:
    #when blake2b hashed with the hash, should be larger than the threshold
    nonce_bytes = nonce.to_bytes(8, byteorder="little")
    blake_obj = blake2b(digest_size=8)
    blake_obj.update(nonce_bytes)
    blake_obj.update(hex_to_bytes(hash))
    #since hex_to_bytes returns big endian, for BANANO_WORK, after we convert to hex, we convert to bytes with big endian
    if int.from_bytes(blake_obj.digest(), byteorder="little") > int.from_bytes(hex_to_bytes(threshold), byteorder="big"):
      #return as big endian
      return bytes_to_hex(bytearray.fromhex(bytes_to_hex(nonce_bytes))[::-1])
    nonce += 1

def gen_work(hash: str) -> str:
  return gen_work_deterministic(hash, BANANO_WORK)

def verify_work(hash: str, work: str) -> bool:
  blake_obj = blake2b(digest_size=8)
  blake_obj.update(bytearray.fromhex(work)[::-1])
  blake_obj.update(hex_to_bytes(hash))
  if int.from_bytes(blake_obj.digest(), byteorder="little") > int.from_bytes(hex_to_bytes(BANANO_WORK), byteorder="big"):
    return True
  else:
    return False
