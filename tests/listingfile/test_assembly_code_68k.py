#!/bin/python3

import unittest
import listingfile.assembly_code_68k

class TestFunction_decode_label(unittest.TestCase):

  def test_all(self):
    label = listingfile.assembly_code_68k.decode_label("                                   TFSGCIA_GEN_OF_CLAWS_ID__3901$SECONDARY:")
    self.assertEqual(label.name, "TFSGCIA_GEN_OF_CLAWS_ID__3901$SECONDARY")
    self.assertEqual(label.line, "                                   TFSGCIA_GEN_OF_CLAWS_ID__3901$SECONDARY:")
    label = listingfile.assembly_code_68k.decode_label("                                   TFSGCIA_GEN_OF_CLAWS_ID__3901$SECONDARY:  ")
    self.assertEqual(label.name, "TFSGCIA_GEN_OF_CLAWS_ID__3901$SECONDARY")
    self.assertEqual(label.line, "                                   TFSGCIA_GEN_OF_CLAWS_ID__3901$SECONDARY:  ")
    label = listingfile.assembly_code_68k.decode_label("                                   ELSE_15:")
    self.assertEqual(label.name, "ELSE_15")
    self.assertEqual(label.line, "                                   ELSE_15:")
    self.assertFalse(listingfile.assembly_code_68k.decode_label("                                   TFSGCIA_GEN_OF_CLAWS_ID__3901$SECONDARY :"))
    self.assertFalse(listingfile.assembly_code_68k.decode_label( "                                  TFSGCIA_GEN_OF_CLAWS_ID__3901$SECONDARY:"))
    self.assertFalse(listingfile.assembly_code_68k.decode_label("                                   TFSGCIA_GEN_OF_CLAWS_ID_+3901$SECONDARY:"))
    
class TestFunction_decode_instruction(unittest.TestCase):

  def test_all(self):
    instruction = listingfile.assembly_code_68k.decode_instruction("     000C  207C *0000000               MOVEA.L     #ADA$TFSSTODP_STORE_HANDLER_$.$DATA,A0")
    self.assertEqual(instruction.address, "000C")
    self.assertEqual(instruction.opcode, "207C *0000000")
    self.assertEqual(instruction.mnemonic, "MOVEA.L")
    self.assertEqual(instruction.arguments, "#ADA$TFSSTODP_STORE_HANDLER_$.$DATA,A0")
    self.assertTrue(listingfile.assembly_code_68k.decode_instruction( "     000C  207C *0000000               MOVEA.L     #ADA$TFSSTODP_STORE_HANDLER_$.$DATA,A0"))
    self.assertFalse(listingfile.assembly_code_68k.decode_instruction( "    000C  207C *0000000               MOVEA.L     #ADA$TFSSTODP_STORE_HANDLER_$.$DATA,A0"))
    self.assertFalse(listingfile.assembly_code_68k.decode_instruction("     000C 207C *0000000                MOVEA.L     #ADA$TFSSTODP_STORE_HANDLER_$.$DATA,A0"))
    self.assertFalse(listingfile.assembly_code_68k.decode_instruction("     000C 207C *0000000               MOVEA.L      #ADA$TFSSTODP_STORE_HANDLER_$.$DATA,A0"))
    self.assertFalse(listingfile.assembly_code_68k.decode_instruction("     0Z0C  20ZC *0000000               MOVEA.L     #ADA$TFSSTODP_STORE_HANDLER_$.$DATA,A0"))