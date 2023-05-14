import pyparsing as pp

class LineOfCode:
  def __init__(self, line):
    self.line = line

class Label(LineOfCode):
  def __init__(self, line, name):
    LineOfCode.__init__(self, line)
    self.name = name

class Instruction(LineOfCode):
  def __init__(self, line, address, opcode, mnemonic, arguments):
    LineOfCode.__init__(self, line)
    self.address = address
    self.opcode = opcode
    self.mnemonic = mnemonic
    self.arguments = arguments

def decode_label(line):
  Label_Name = pp.Word(pp.alphanums + "_$")
  Label_Code = pp.Literal("                                   ").suppress() + Label_Name + pp.Literal(":").suppress()
  Label_Code.leaveWhitespace()
  try:
    finding = Label_Code.parseString(str(line).rstrip(), parseAll=True)[0]
    return Label(line, line[35:35+len(finding)])
  except pp.ParseException:
    return False

def decode_instruction(line):
  if not(str(line).startswith("     ")):
    return False
  parsed_line = line[5:]
  if len(parsed_line) < 6 or str(parsed_line[4:6]) != "  ":
    return False
  try:
    int(str(parsed_line[:4]), 16)
    address = parsed_line[:4]
  except ValueError:
    return False
  parsed_line = parsed_line[6:]
  if len(parsed_line) < 28:
    return False
  opcode = str(parsed_line[:28]).rstrip()
  opcode = parsed_line[:28][:len(opcode)]
  parsed_line = parsed_line[28:]
  if len(parsed_line) < 12:
    return False
  mnemonic = str(parsed_line[:12]).rstrip()
  mnemonic = parsed_line[:12][:len(mnemonic)]
  parsed_line = parsed_line[12:]
  arguments = str(parsed_line).rstrip()
  arguments = parsed_line[:len(arguments)]
  return Instruction(line, address, opcode, mnemonic, arguments)
