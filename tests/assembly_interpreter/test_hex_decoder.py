#!/bin/python3
 
import unittest
import assembly_interpreter.hex_decoder


class TestFunction_make_byte_sequence_from_hex_string(unittest.TestCase):

  def test_empty(self):
    x = assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("")
    self.assertEqual(str(x), "")

  def test_bytes(self):
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("0"), "0x0")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("1"), "0x1")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("2"), "0x2")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("9"), "0x9")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("A"), "0xA")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("F"), "0xF")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("00"), "0x00")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("01"), "0x01")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("02"), "0x02")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("0F"), "0x0F")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("10"), "0x10")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("F0"), "0xF0")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("FF"), "0xFF")
    
  def test_spaces(self):
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string(" 0"), "0x0")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string(" 1"), "0x1")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string(" 2"), "0x2")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("    9"), "0x9")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string(" A"), "0xA")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string(" F"), "0xF")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string(" 0"), "0x0")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("1 "), "0x1")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("   2 "), "0x2")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string(" 9   "), "0x9")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("A "), "0xA")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("F "), "0xF")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string(" 00"), "0x00")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("0 1"), "0x01")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("02 "), "0x02")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string(" 0 F "), "0x0F")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("  1  0  "), "0x10")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("F0  "), "0xF0")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("FF  "), "0xFF")

  def test_sequence(self):
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("01 2 34 5 6 789 AB C D E F"), "0x0123456789ABCDEF")

  def test_number(self):
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("*0000000"), "0x00000000")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("0 *0000000"), "0x000000000")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("00 *0000000 00"), "0x000000000000")
    self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("AA *0000000 FF"), "0xAA00000000FF")


  def test_incorrec(self):
    with self.assertRaises(ValueError):
      self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("G"), "0x0")
    with self.assertRaises(ValueError):
      self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("*0"), "0x0")
    with self.assertRaises(ValueError):
      self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("4;"), "0x0")
    with self.assertRaises(ValueError):
      self.assertEqual(assembly_interpreter.hex_decoder.make_byte_sequence_from_hex_string("3."), "0x0")

