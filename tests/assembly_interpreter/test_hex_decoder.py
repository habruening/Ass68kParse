#!/bin/python3
 
import unittest
import assembly_interpreter.hex_decoder


class TestFunction_make_bits_from_hex_string(unittest.TestCase):

  def test_empty(self):
    x = assembly_interpreter.hex_decoder.make_bits_from_hex_string("")
    self.assertEqual(str(x), "")

  def test_bytes(self):
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("0"), "0x0")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("1"), "0x1")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("2"), "0x2")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("9"), "0x9")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("A"), "0xA")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("F"), "0xF")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("00"), "0x00")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("01"), "0x01")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("02"), "0x02")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("0F"), "0x0F")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("10"), "0x10")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("F0"), "0xF0")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("FF"), "0xFF")
    
  def test_spaces(self):
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string(" 0"), "0x0")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string(" 1"), "0x1")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string(" 2"), "0x2")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("    9"), "0x9")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string(" A"), "0xA")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string(" F"), "0xF")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string(" 0"), "0x0")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("1 "), "0x1")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("   2 "), "0x2")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string(" 9   "), "0x9")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("A "), "0xA")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("F "), "0xF")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string(" 00"), "0x00")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("0 1"), "0x01")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("02 "), "0x02")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string(" 0 F "), "0x0F")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("  1  0  "), "0x10")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("F0  "), "0xF0")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("FF  "), "0xFF")

  def test_sequence(self):
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("01 2 34 5 6 789 AB C D E F"), "0x0123456789ABCDEF")

  def test_number(self):
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("*0000000"), "0x00000000")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("0 *0000000"), "0x000000000")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("00 *0000000 00"), "0x000000000000")
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("AA *0000000 FF"), "0xAA00000000FF")


  def test_incorrect(self):
    with self.assertRaises(ValueError):
      self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("G"), "0x0")
    with self.assertRaises(ValueError):
      self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("*0"), "0x0")
    with self.assertRaises(ValueError):
      self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("4;"), "0x0")
    with self.assertRaises(ValueError):
      self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("3."), "0x0")

class TestFunction_ensure_is_bits(unittest.TestCase):
  def test_ensure_is_bits(self):
    self.assertEqual(assembly_interpreter.hex_decoder.ensure_is_bits("0xE")[0],1)
    self.assertEqual(assembly_interpreter.hex_decoder.ensure_is_bits("0xE")[1],1)
    self.assertEqual(assembly_interpreter.hex_decoder.ensure_is_bits("0xE")[2],1)
    self.assertEqual(assembly_interpreter.hex_decoder.ensure_is_bits("0xE")[3],0)
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("0xE")[0],1)
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("0xE")[1],1)
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("0xE")[2],1)
    self.assertEqual(assembly_interpreter.hex_decoder.make_bits_from_hex_string("0xE")[3],0)

class TestFunction_extend_bits_to_length(unittest.TestCase):
  def test_extend_bits_to_length(self):
    x = assembly_interpreter.hex_decoder.extend_bits_to_length(assembly_interpreter.hex_decoder.make_bits_from_hex_string(""),8)
    self.assertEqual(x.len, 8)
    x = assembly_interpreter.hex_decoder.extend_bits_to_length(assembly_interpreter.hex_decoder.make_bits_from_hex_string("00"),8)
    self.assertEqual(x.len, 8)
    x = assembly_interpreter.hex_decoder.extend_bits_to_length(assembly_interpreter.hex_decoder.make_bits_from_hex_string("AA"),8)
    self.assertEqual(x.len, 8)
    x = assembly_interpreter.hex_decoder.extend_bits_to_length(assembly_interpreter.hex_decoder.make_bits_from_hex_string("AA"),9)
    self.assertEqual(x.len, 9)


class TestFunction_extract_bits(unittest.TestCase):
  def test_extract_bits(self):
    tester = lambda data, mask : \
      assembly_interpreter.hex_decoder.extract_bits(assembly_interpreter.hex_decoder.ensure_is_bits(data), mask)
    self.assertEqual(tester("0b0101", "0b0101"), "0b11")
    self.assertEqual(tester("0b0101", "0b1001"), "0b01")
    self.assertEqual(tester("0b0111", "0b1001"), "0b01")
    self.assertEqual(tester("0b1000", "0b1001"), "0b10")


class TestFunction_check_bits(unittest.TestCase):
  def test_check_bits(self):
    tester = lambda data, mask, check : \
      assembly_interpreter.hex_decoder.check_bits(assembly_interpreter.hex_decoder.ensure_is_bits(data), mask, check)
    self.assertTrue(tester("0b0101", "0b0101", "0b11"))
    self.assertTrue(tester("0b0101", "0b1001", "0b01"))
    self.assertTrue(tester("0b0111", "0b1001", "0b01"))
    self.assertTrue(tester("0b1000", "0b1001", "0b10"))
    
class TestFunction_as_undecoded(unittest.TestCase):
  def test_as_undecoded(self):
    x = assembly_interpreter.hex_decoder.make_bits_from_hex_string("AA")
    y = assembly_interpreter.hex_decoder.as_undecoded(x)
    self.assertEqual(y, assembly_interpreter.hex_decoder.make_bits_from_hex_string("FF"))

class TestFunction_make_undecoded_opcode_from_hex_string(unittest.TestCase):
  def test_make_undecoded_opcode_from_hex_string(self):
    self.assertEqual(assembly_interpreter.hex_decoder.make_undecoded_opcode_from_hex_string("1A")["opcode"], "0x1A")
    self.assertEqual(assembly_interpreter.hex_decoder.make_undecoded_opcode_from_hex_string("1A")["undecoded"], "0xFF")

class TestFunction_set_decoded_in_opcode(unittest.TestCase):
  def test_set_decoded_in_opcode(self):
    x = assembly_interpreter.hex_decoder.make_undecoded_opcode_from_hex_string("1A")
    self.assertEqual(assembly_interpreter.hex_decoder.set_decoded_in_opcode(x, "0x0F")["undecoded"], "0xF0")
    self.assertEqual(assembly_interpreter.hex_decoder.set_decoded_in_opcode(x, "0xFF")["undecoded"], "0x00")
    self.assertEqual(assembly_interpreter.hex_decoder.set_decoded_in_opcode(x, "0x00")["undecoded"], "0xFF")

class TestFunction_decode_from_opcode(unittest.TestCase):
  def test_decode_from_opcode(self):
    x = assembly_interpreter.hex_decoder.make_undecoded_opcode_from_hex_string("1A") # 00011010
    y = assembly_interpreter.hex_decoder.decode_from_opcode(x, "0b0001101", "0b111")
    self.assertEqual(y["extracted_bits"], "0b111")
    self.assertEqual(y["opcode_with_undecoded"]["undecoded"], "0b11100101")
    self.assertFalse(assembly_interpreter.hex_decoder.decode_from_opcode(x, "0b0001101", "0b101"))

class TestFunction_decode_and_get_from_opcode(unittest.TestCase):
  def test_decode_and_get_from_opcode(self):
    x = assembly_interpreter.hex_decoder.make_undecoded_opcode_from_hex_string("1A") # 00011010
    y = assembly_interpreter.hex_decoder.decode_and_get_from_opcode(x, "0b0001101")
    self.assertEqual(y["extracted_bits"], "0b111")
    self.assertEqual(y["opcode_with_undecoded"]["undecoded"], "0b11100101")
    self.assertFalse(assembly_interpreter.hex_decoder.decode_from_opcode(x, "0b0001101", "0b101"))
