#!/bin/python3

import unittest
import listingfile.listing_file_68k

class TestLogger():
  def __init__(self):
    self.warnings = []
  def warning(self, message):
    self.warnings.append(message)

listingfile.listing_file_68k.log = TestLogger()

class LineStub:
  def __init__(self, text):
    self.line = text
  def text(self):
    return self.line

def create_page_stub(text):
  return list(map(lambda x:LineStub(x), text.splitlines()))

class TestFunction_check_page_header(unittest.TestCase):

  def test_empty_file(self):
    listingfile.listing_file_68k.log.warnings = []
    header_correct = listingfile.listing_file_68k.check_page_header(1, [])
    self.assertTrue(header_correct)
    self.assertFalse(listingfile.listing_file_68k.log.warnings)

  def test_examples(self):
    listingfile.listing_file_68k.log.warnings = []
    with open("tests/listingfile/TestData/PageHeaderTests.txt", "r") as input:
      tests = input.read().splitlines()
      line = 0
      while line < len(tests):
        header = tests[line] + "\n" + tests[line+1]
        warning = tests[line+2]
        listingfile.listing_file_68k.log.warnings = []
        header_correct = listingfile.listing_file_68k.check_page_header(1, create_page_stub(header))
        if not warning:
          self.assertTrue(header_correct)
          self.assertFalse(listingfile.listing_file_68k.log.warnings)
        else:
          self.assertFalse(header_correct)
          self.assertTrue(listingfile.listing_file_68k.log.warnings)
          self.assertIn(warning, listingfile.listing_file_68k.log.warnings[0])
        line = line + 4

  def test_num_lines(self):
    listingfile.listing_file_68k.log.warnings = []
    with open("tests/listingfile/TestData/PageHeaderTests.txt", "r") as input:
      tests = input.read().splitlines()
      header = tests[0] + "\n" + tests[0+1]
      test = header + "\n" + "\n".join([str(i) for i in range(1,59)])
      listingfile.listing_file_68k.log.warnings = []
      header_correct = listingfile.listing_file_68k.check_page_header(1, create_page_stub(test))
      self.assertTrue(header_correct)
      self.assertFalse(listingfile.listing_file_68k.log.warnings)
      test = test + "\n" + "59"
      header_correct = listingfile.listing_file_68k.check_page_header(1, create_page_stub(test))
      self.assertFalse(header_correct)
      self.assertIn("too many lines", listingfile.listing_file_68k.log.warnings[0])
         