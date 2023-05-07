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
  line = line[5:]
  if len(line) < 6 or str(line[4:6]) != "  ":
    return False
  try:
    int(str(line[:4]), 16)
    address = line[:4]
  except ValueError:
    return False
  line = line[6:]
  if len(line) < 28:
    return False
  opcode = str(line[:28]).rstrip()
  opcode = line[:28][:len(opcode)]
  line = line[28:]
  if len(line) < 12:
    return False
  mnemonic = str(line[:12]).rstrip()
  mnemonic = line[:12][:len(mnemonic)]
  line = line[12:]
  arguments = str(line).rstrip()
  arguments = line[:len(arguments)]
  return Instruction(line, address, opcode, mnemonic, arguments)
