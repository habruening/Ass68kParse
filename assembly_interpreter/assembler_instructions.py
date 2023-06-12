import assembly_interpreter.hex_decoder as aih

def get_field_value(decoded_instruction, field_name):
  return decoded_instruction[field_name]["extracted_bits"]

def identify_field_of_bit_no(decoded_instruction, bit_no):
  for key, value in decoded_instruction.items():
    if key == "name":
      continue
    if bit_no < len(value["mask"]) and value["mask"][bit_no]:
      return key

moveq_instruction = ("MOVEQ", {"moveq" : ("0b11110001", "0b01110"),
                               "register" : "0b0000111",
                               "data" : "0x00FF"})

def decode_instruction_from_format(opcode, instruction_format):
  decoding = aih.make_undecoded_opcode_from_hex_string(opcode)
  result = {"name" : instruction_format[0]}
  for field, rule in instruction_format[1].items():
    if isinstance(rule, tuple):
      decoding = aih.decode_from_opcode(decoding, rule[0], rule[1])
      if not(decoding):
        return False
    else:
      decoding = aih.decode_and_get_from_opcode(decoding, rule)
    result[field] = decoding   
  return result
  
def decode_moveq(opcode):
  return decode_instruction_from_format(opcode, moveq_instruction)

def decode_move(opcode):
  undecoded_instruction = aih.make_undecoded_opcode_from_hex_string(opcode)
  move_decoded = aih.decode_from_opcode(undecoded_instruction, "0b11", "0b00")
  if not(move_decoded):
    return False
  size_decoded = aih.decode_and_get_from_opcode(move_decoded, "0b0011")
  destination_register_decoded = aih.decode_and_get_from_opcode(size_decoded, "0b0000111")
  destination_mode_decoded = aih.decode_and_get_from_opcode(destination_register_decoded, "0b0000000111")
  source_mode_decoded = aih.decode_and_get_from_opcode(destination_mode_decoded, "0b0000000000111")
  source_register_decoded = aih.decode_and_get_from_opcode(source_mode_decoded, "0b0000000000000111")
  return {"name" : "MOVE", "move" : move_decoded, "size" : size_decoded,
          "destination_register" : destination_register_decoded, "destination_mode" : destination_mode_decoded,
          "source_mode" : source_mode_decoded, "source_register" : source_register_decoded}

def decode_instruction(opcode):
  if (instruction := decode_moveq(opcode)):
    return instruction
  if (instruction := decode_move(opcode)):
    return instruction