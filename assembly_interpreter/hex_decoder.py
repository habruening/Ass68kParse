from bitstring import *

def make_byte_sequence_from_hex_string(hex_string):
  hex_string = hex_string.split()
  result = BitArray()
  for word in hex_string:
    if word == "*0000000":
      word = "00000000"
    result.append(BitArray(hex = word))
  return result

