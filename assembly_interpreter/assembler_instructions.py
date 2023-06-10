import assembly_interpreter.hex_decoder

def map_bit(decoded_instruction, bit_no):
  for field in decoded_instruction.keys():
    if field == "name":
      continue
    if bit_no < len(decoded_instruction[field]["mask"]) and decoded_instruction[field]["mask"][bit_no]:
      return field

def decode_moveq(opcode):
  undecoded_instruction = assembly_interpreter.hex_decoder.make_undecoded_opcode_from_hex_string(opcode)
  moveq_decoded = assembly_interpreter.hex_decoder.decode_from_opcode(undecoded_instruction, "0b11110001", "0b01110")
  if not(moveq_decoded):
    return False
  register_decoded = assembly_interpreter.hex_decoder.decode_and_get_from_opcode(moveq_decoded, "0b0000111")
  data_decoded = assembly_interpreter.hex_decoder.decode_and_get_from_opcode(register_decoded, "0x00FF")
  return {"name" : "MOVEQ", "moveq" : moveq_decoded, "register" : register_decoded, "data" : data_decoded}

def decode_move(opcode):
  undecoded_instruction = assembly_interpreter.hex_decoder.make_undecoded_opcode_from_hex_string(opcode)
  move_decoded = assembly_interpreter.hex_decoder.decode_from_opcode(undecoded_instruction, "0b11", "0b00")
  if not(move_decoded):
    return False
  size_decoded = assembly_interpreter.hex_decoder.decode_and_get_from_opcode(move_decoded, "0b0011")
  destination_register_decoded = assembly_interpreter.hex_decoder.decode_and_get_from_opcode(size_decoded, "0b0000111")
  destination_mode_decoded = assembly_interpreter.hex_decoder.decode_and_get_from_opcode(destination_register_decoded, "0b0000000111")
  source_mode_decoded = assembly_interpreter.hex_decoder.decode_and_get_from_opcode(destination_mode_decoded, "0b0000000000111")
  source_register_decoded = assembly_interpreter.hex_decoder.decode_and_get_from_opcode(source_mode_decoded, "0b0000000000000111")
  return {"name" : "MOVE", "move" : move_decoded, "size" : size_decoded,
          "destination_register" : destination_register_decoded, "destination_mode" : destination_mode_decoded,
          "source_mode" : source_mode_decoded, "source_register" : source_register_decoded}

def decode_instruction(opcode):
  if (instruction := decode_moveq(opcode)):
    return instruction
  if (instruction := decode_move(opcode)):
    return instruction