from bitstring import *

def make_bits_from_hex_string(hex_string):
  hex_string = hex_string.split()
  result = Bits()
  for word in hex_string:
    if word == "*0000000":
      word = "00000000"
    result = result + Bits(hex = word)
  return result

def ensure_is_bits(guess):
  if isinstance(guess, str):
    return Bits(guess)
  return guess

def extend_bits_to_length(bits, length):
  return bits + Bits(length - bits.len)

def extract_bits(bits, mask):
  mask = ensure_is_bits(mask)
  extracted_bits = [Bits(bool=i) for i,j in zip(bits, mask) if j]
  extracted_bits = Bits().join(extracted_bits)
  return extracted_bits

def check_bits(bits, mask, check):
  mask = ensure_is_bits(mask)
  check = ensure_is_bits(check)
  extracted_bits = extract_bits(bits, mask)
  return extracted_bits == check

def as_undecoded(bits):
  return ~Bits(length = bits.len)
  
def make_undecoded_opcode_from_hex_string(hex_string):
  opcode = make_bits_from_hex_string(hex_string)
  return {"opcode" : opcode, "undecoded" : as_undecoded(opcode)}

def set_decoded_in_opcode(opcode_with_undecoded, decoded_bits):
  decoded_bits = extend_bits_to_length(ensure_is_bits(decoded_bits), opcode_with_undecoded["undecoded"].len)
  return opcode_with_undecoded | { "undecoded" : opcode_with_undecoded["undecoded"] & ~decoded_bits }

def make_opcode_extraction(opcode_with_undecoded, extracted_bits, mask):
  return {"opcode_with_undecoded" : opcode_with_undecoded, "extracted_bits" : extracted_bits, "mask" : ensure_is_bits(mask)}

def decode_from_opcode(opcode_with_undecoded, mask, check):
  if("opcode_with_undecoded" in opcode_with_undecoded.keys()):
    opcode_with_undecoded = opcode_with_undecoded["opcode_with_undecoded"]
  if check_bits(opcode_with_undecoded["opcode"], mask, check):
    return make_opcode_extraction(set_decoded_in_opcode(opcode_with_undecoded, mask), check, mask)
  return False

def decode_and_get_from_opcode(opcode_with_undecoded, mask):
  if("opcode_with_undecoded" in opcode_with_undecoded.keys()):
    opcode_with_undecoded = opcode_with_undecoded["opcode_with_undecoded"]
  result = extract_bits(opcode_with_undecoded["opcode"], mask)
  return make_opcode_extraction(set_decoded_in_opcode(opcode_with_undecoded, mask), result, mask)