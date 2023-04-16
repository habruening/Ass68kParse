#!/bin/python3
 
import unittest
import assembly_viewer.format_as_block

class TestClassTranslator(unittest.TestCase):
  
  def test_create_mapping(self):
    mapping = assembly_viewer.format_as_block.Translator.create_mapping(1,2)
    self.assertEqual(mapping["source"], 1)
    self.assertEqual(mapping["target"], 2)

  def test_constructor(self):
    mapping = assembly_viewer.format_as_block.Translator()
    self.assertEqual(len(mapping.mapping), 1)
    self.assertEqual(mapping.mapping[0], {"source": 0, "target" : 0})

  def test_method_add_mapping(self):
    mapping = assembly_viewer.format_as_block.Translator()
    mapping.add_mapping(0,1)
    mapping.add_mapping(1,2)
    mapping.add_mapping(3,6)
    self.assertEqual(len(mapping.mapping), 4)
    self.assertEqual(mapping.mapping[0], {"source": 0, "target" : 0})
    self.assertEqual(mapping.mapping[1], {"source": 0, "target" : 1})
    self.assertEqual(mapping.mapping[2], {"source": 1, "target" : 3})
    self.assertEqual(mapping.mapping[3], {"source": 4, "target" : 9})

  def test_method_source_to_target(self):
    mapping = assembly_viewer.format_as_block.Translator()
    mapping.add_mapping(0,1) # 0 1
    mapping.add_mapping(1,2) # 1 3
    mapping.add_mapping(3,6) # 4 9
    mapping.add_mapping(3,3) # 7 12
    self.assertEqual(mapping.source_to_target(0), 1)
    self.assertEqual(mapping.source_to_target(1), 3)
    self.assertEqual(mapping.source_to_target(2), 4)
    self.assertEqual(mapping.source_to_target(3), 5)
    self.assertEqual(mapping.source_to_target(4), 9)
    self.assertEqual(mapping.source_to_target(5), 10)
    self.assertEqual(mapping.source_to_target(6), 11)
    self.assertEqual(mapping.source_to_target(7), 12)

  def test_method_target_to_source(self):
    mapping = assembly_viewer.format_as_block.Translator()
    mapping.add_mapping(0,1) # 0 1
    mapping.add_mapping(1,2) # 1 3
    mapping.add_mapping(3,6) # 4 9
    mapping.add_mapping(3,3) # 7 12
    #     0 123   456
    # -> -0-123---456 
    self.assertEqual(mapping.target_to_source(0), 0)
    self.assertEqual(mapping.target_to_source(1), 0)
    self.assertEqual(mapping.target_to_source(2), 1)
    self.assertEqual(mapping.target_to_source(3), 1)
    self.assertEqual(mapping.target_to_source(4), 2)
    self.assertEqual(mapping.target_to_source(5), 3)
    self.assertEqual(mapping.target_to_source(6), 4)
    self.assertEqual(mapping.target_to_source(7), 4)
    self.assertEqual(mapping.target_to_source(8), 4)
    self.assertEqual(mapping.target_to_source(9), 4)
    self.assertEqual(mapping.target_to_source(10), 5)
    self.assertEqual(mapping.target_to_source(11), 6)

class TestFunction_adjust_line_length(unittest.TestCase):

  def test_all(self):
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("", 10)[0],         "          ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" ", 10)[0],        "          ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\n", 10)[0],       "          \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\r\n", 10)[0],     "          \r\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a", 10)[0],        "a         ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\n", 10)[0],      "a         \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\r\n", 10)[0],    "a         \r\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a ", 10)[0],       "a         ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \n", 10)[0],     "a         \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \r\n", 10)[0],   "a         \r\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\f", 10)[0],       "          \f")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\f\n", 10)[0],     "          \f\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\r\n\f", 10)[0],   "          \r\n\f")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\f", 10)[0],      "a         \f")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\f\n", 10)[0],    "a         \f\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\f\r\n", 10)[0],  "a         \f\r\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \f", 10)[0],     "a         \f")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \f\n", 10)[0],   "a         \f\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \f\r\n", 10)[0], "a         \f\r\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" \n", 10)[0],      "          \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" \r\n", 10)[0],    "          \r\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a", 10)[0],       " a        ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\n", 10)[0],     " a        \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\r\n", 10)[0],   " a        \r\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a ", 10)[0],      " a        ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a \n", 10)[0],    " a        \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a \r\n", 10)[0],  " a        \r\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" \f", 10)[0],      "          \f")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" \f\n", 10)[0],    "          \f\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" \r\n\f", 10)[0],  "          \r\n\f")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\f", 10)[0],     " a        \f")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\f\n", 10)[0],   " a        \f\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\f\r\n", 10)[0], " a        \f\r\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a \f", 10)[0],    " a        \f")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a \f\n", 10)[0],  " a        \f\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a \f\r\n", 10)[0]," a        \f\r\n")

  def test_tabulators(self):
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t", 10)[0],        "          ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\t", 10)[0],       "a         ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\t", 10)[0],      " a        ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \t", 10)[0],      "a         ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t", 10)[0],        "          ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\t", 10)[0],       "a         ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\t", 10)[0],      " a        ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\tb", 10)[0],       "        b ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\tb", 10)[0],      "a       b ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\tb", 10)[0],     " a      b ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \tb", 10)[0],     "a       b ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\tb", 10)[0],       "        b ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\tb", 10)[0],      "a       b ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\tb", 10)[0],     " a      b ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \tb", 10)[0],     "a       b ")

    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t\t", 20)[0],      "                    ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\t\t", 20)[0],     "a                   ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\ta\t", 20)[0],     "        a           ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t\ta", 20)[0],     "                a   ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\tb\t", 20)[0],    "a       b           ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\t\tb", 20)[0],    "a               b   ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\ta\tb", 20)[0],    "        a       b   ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\tb\tc", 20)[0],   "a       b       c   ")

    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t\t", 10, 3)[0],      "          ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\t\t", 10, 3)[0],     "a         ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\ta\t", 10, 3)[0],     "   a      ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t\ta", 10, 3)[0],     "      a   ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\tb\t", 10, 3)[0],    "a  b      ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\t\tb", 10, 3)[0],    "a     b   ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\ta\tb", 10, 3)[0],    "   a  b   ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\tb\tc", 10, 3)[0],   "a  b  c   ")

    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t\n", 10)[0],        "          \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\t\n", 10)[0],       "a         \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\t\n", 10)[0],      " a        \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \t\n", 10)[0],      "a         \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t\n", 10)[0],        "          \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\t\n", 10)[0],       "a         \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\t\n", 10)[0],      " a        \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\tb\n", 10)[0],       "        b \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\tb\n", 10)[0],      "a       b \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\tb\n", 10)[0],     " a      b \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \tb\n", 10)[0],     "a       b \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\tb\n", 10)[0],       "        b \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\tb\n", 10)[0],      "a       b \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length(" a\tb\n", 10)[0],     " a      b \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a \tb\n", 10)[0],     "a       b \n")

    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t\t\n", 20)[0],      "                    \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\t\t\n", 20)[0],     "a                   \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\ta\t\n", 20)[0],     "        a           \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t\ta\n", 20)[0],     "                a   \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\tb\t\n", 20)[0],    "a       b           \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\t\tb\n", 20)[0],    "a               b   \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\ta\tb\n", 20)[0],    "        a       b   \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("a\tb\tc\n", 20)[0],   "a       b       c   \n")

  def test_oversize(self):
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("          ", 5)[0],      "          ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("abcdefghij", 5)[0],      "abcdefghij")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t", 5)[0],              "        ")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\ta", 5)[0],             "        a")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("          \n", 5)[0],    "          \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("abcdefghij\n", 5)[0],    "abcdefghij\n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\t\n", 5)[0],            "        \n")
    self.assertEqual(assembly_viewer.format_as_block.adjust_line_length("\ta\n", 5)[0],           "        a\n")
    
class TestFunction_adjust_line_lengths(unittest.TestCase):

  def test_all(self):
    lines = assembly_viewer.format_as_block.adjust_line_lengths("aaaa\nbbbb\ncccc", 3)
    self.assertEqual(lines["text"],"aaaa\nbbbb\ncccc")
    
    lines = assembly_viewer.format_as_block.adjust_line_lengths("aaaa\nbbbb\ncccc", 5)
    self.assertEqual(lines["text"],"aaaa \nbbbb \ncccc ")
    
    lines = assembly_viewer.format_as_block.adjust_line_lengths("aaaaaaaa\nbbbb\ncccc", 5)
    self.assertEqual(lines["text"],"aaaaaaaa\nbbbb \ncccc ")
    
    lines = assembly_viewer.format_as_block.adjust_line_lengths("a\ta\nbbbb\ncccc", 5)
    self.assertEqual(lines["text"],"a       a\nbbbb \ncccc ")
    
  def test_empty_text(self):
    lines = assembly_viewer.format_as_block.adjust_line_lengths("", 3)
    self.assertEqual(lines["text"],"")
    
    lines = assembly_viewer.format_as_block.adjust_line_lengths("\n", 3)
    self.assertEqual(lines["text"],"   \n")
    
    lines = assembly_viewer.format_as_block.adjust_line_lengths("\n\n", 3)
    self.assertEqual(lines["text"],"   \n   \n")
    
class TestClass_TextAsBlock(unittest.TestCase):

  def test_construction(self):
    # This is a white box test. Only for debgging.
    block = assembly_viewer.format_as_block.TextAsBlock("aaaa\nb\nc\tc\n", 3)
    self.assertEqual(block.text,"aaaa\nb  \nc       c\n")

  def test_get_block_offset(self):
    block = assembly_viewer.format_as_block.TextAsBlock("aaaa\nb\nc\tc\n", 3)
    self.assertEqual(block.text,"aaaa\nb  \nc       c\n")
    self.assertEqual(block.translator.source_to_target(0), 0)
    self.assertEqual(block.translator.source_to_target(1), 1)
    self.assertEqual(block.translator.source_to_target(4), 4)
    self.assertEqual(block.translator.source_to_target(5), 5)
    self.assertEqual(block.translator.source_to_target(6), 6)
    self.assertEqual(block.translator.source_to_target(7), 9)
    self.assertEqual(block.translator.source_to_target(8), 10)
    self.assertEqual(block.translator.source_to_target(9), 11)
    self.assertEqual(block.translator.source_to_target(10), 18)
     
  def test_get_original_offset(self):
    block = assembly_viewer.format_as_block.TextAsBlock("aaaa\nb\nc\tc\n", 3)
    self.assertEqual(block.text,"aaaa\nb  \nc       c\n")
    self.assertEqual(block.translator.target_to_source(0), 0)
    self.assertEqual(block.translator.target_to_source(1), 1)
    self.assertEqual(block.translator.target_to_source(4), 4)
    self.assertEqual(block.translator.target_to_source(5), 5)
    self.assertEqual(block.translator.target_to_source(6), 6)
    self.assertEqual(block.translator.target_to_source(7), 6)
    self.assertEqual(block.translator.target_to_source(8), 6)
    self.assertEqual(block.translator.target_to_source(9), 7)
    self.assertEqual(block.translator.target_to_source(9), 7)
    self.assertEqual(block.translator.target_to_source(10), 9)
    self.assertEqual(block.translator.target_to_source(16), 9)
    self.assertEqual(block.translator.target_to_source(19), 11)