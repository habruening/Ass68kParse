
from listingfile import listing_file_68k
from listingfile import assembly_code_68k

def open_assembly_file(file_name):

  all_lines_orig = listing_file_68k.open_file(file_name)

  all_lines = []
  assembler_code = []
  for line in all_lines_orig:
    if assembly_code_68k.decode_instruction(line):
      instruction = assembly_code_68k.decode_instruction(line)
      instruction.lines = line.lines
      all_lines.append(instruction)
      assembler_code.append(instruction)
      instruction.go_to = []
    elif assembly_code_68k.decode_label(line):
      label = assembly_code_68k.decode_label(line)
      label.lines = line.lines
      all_lines.append(label)
      assembler_code.append(label)
      label.come_from = []
    else:
      all_lines.append(line)

  for label in (l for l in assembler_code if type(l) == assembly_code_68k.Label):
    for instruction in (i for i in assembler_code if type(i) == assembly_code_68k.Instruction):
      if(str(label.name) == str(instruction.arguments)):
        instruction.go_to.append(label)
        label.come_from.append(instruction)

  return all_lines
