import assembly_interpreter.hex_decoder as aih

def get_field_value(decoded_instruction, field_name):
  return decoded_instruction[field_name]["extracted_bits"]

def identify_field_of_bit_no(decoded_instruction, bit_no):
  for key, value in decoded_instruction.items():
    if key == "name":
      continue
    if bit_no < len(value["mask"]) and value["mask"][bit_no]:
      return key

moveq_instruction = ("MOVEQ", {"moveq"    : ("0b11110001", "0b01110"),
                               "register" :  "0b0000111",
                               "data"     :  "0x00FF"})

move_instruction =  ("MOVE",  {"move"                 : ("0b11", "0b00"),
                               "size"                 :  "0b0011",
                               "destination_register" :  "0b0000111",
                               "destination_mode"     :  "0b0000000111",
                               "source_mode"          :  "0b0000000000111",
                               "source_register"      :  "0b0000000000000111"})

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
  
def decode_instruction(opcode):
  if (instruction := decode_instruction_from_format(opcode, move_instruction)):
    return instruction
  if (instruction := decode_instruction_from_format(opcode, moveq_instruction)):
    return instruction