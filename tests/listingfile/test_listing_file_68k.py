#!/bin/python3

import unittest
import listingfile.listing_file_68k

class LoggerStub():
  def __init__(self):
    self.warnings = []
  def warning(self, message):
    self.warnings.append(message)

listingfile.listing_file_68k.log = LoggerStub()

class LineStub:
  def __init__(self, text):
    self.line = text
  def text(self):
    return self.line
  
def lines_to_string(lines):
  return "".join([line.text() for line in lines])

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
         

def check_page_header_stub(page_no, page, logger = False):
  if len(page)<2:
    return False
  if (page[0].text() != "a") or (page[1].text() != "b"):
    return False
  return True
  
def test_reconstruct_lost_pages_with(text):
  pages = listingfile.listing_file_68k.reconstruct_lost_pages(17, [LineStub(l) for l in text])
  return ["".join([l.text() for l in p]) for p in pages]

class TestFunction_reconstruct_lost_pages(unittest.TestCase):

  def test_examples(self):
    original_check_page_header = listingfile.listing_file_68k.check_page_header
    listingfile.listing_file_68k.check_page_header = check_page_header_stub
    self.assertEqual(test_reconstruct_lost_pages_with(""), [])
    self.assertEqual(test_reconstruct_lost_pages_with("x"), ["x"])
    self.assertEqual(test_reconstruct_lost_pages_with("xab"), ["x", "ab"])
    self.assertEqual(test_reconstruct_lost_pages_with("a"), ["a"])
    self.assertEqual(test_reconstruct_lost_pages_with("ab"), ["ab"])
    self.assertEqual(test_reconstruct_lost_pages_with("aba"), ["aba"])
    self.assertEqual(test_reconstruct_lost_pages_with("abab"), ["ab", "ab"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxab"), ["abx", "ab"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxabx"), ["abx", "abx"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxababx"), ["abx", "ab", "abx"])
    listingfile.listing_file_68k.check_page_header = original_check_page_header

  def test_warning_messages(self):
    listingfile.listing_file_68k.log.warnings = []
    original_check_page_header = listingfile.listing_file_68k.check_page_header
    listingfile.listing_file_68k.check_page_header = check_page_header_stub
    test_reconstruct_lost_pages_with("")
    self.assertFalse(listingfile.listing_file_68k.log.warnings)
    test_reconstruct_lost_pages_with("abxxxx")
    self.assertFalse(listingfile.listing_file_68k.log.warnings)
    # The following one is no error, because this is already checked by listingfile.listing_file_68k.check_page_header
    test_reconstruct_lost_pages_with("x")
    self.assertFalse(listingfile.listing_file_68k.log.warnings)
    test_reconstruct_lost_pages_with("xab")
    self.assertIn("Reconstructing page", listingfile.listing_file_68k.log.warnings[0])
    listingfile.listing_file_68k.log.warnings = []
    test_reconstruct_lost_pages_with("abxab")
    self.assertIn("Reconstructing page", listingfile.listing_file_68k.log.warnings[0])
    listingfile.listing_file_68k.check_page_header = original_check_page_header

def test_make_pages_with(text):
  pages = listingfile.listing_file_68k.make_pages(17, [LineStub(l) for l in text])
  return ["header:"+lines_to_string(page["header"])+",content:"+lines_to_string(page["content"]) for page in pages]

class TestFunction_make_pages(unittest.TestCase):

  def test_all(self):
    original_check_page_header = listingfile.listing_file_68k.check_page_header
    listingfile.listing_file_68k.check_page_header = check_page_header_stub
    self.assertEqual(test_make_pages_with(""),         [])
    self.assertEqual(test_make_pages_with("x"),        ["header:,content:x"])
    self.assertEqual(test_make_pages_with("xab"),      ["header:,content:x", "header:ab,content:"])
    self.assertEqual(test_make_pages_with("a"),        ["header:,content:a"])
    self.assertEqual(test_make_pages_with("ab"),       ["header:ab,content:"])
    self.assertEqual(test_make_pages_with("aba"),      ["header:ab,content:a"])
    self.assertEqual(test_make_pages_with("abab"),     ["header:ab,content:", "header:ab,content:"])
    self.assertEqual(test_make_pages_with("abxab"),    ["header:ab,content:x", "header:ab,content:"])
    self.assertEqual(test_make_pages_with("abxabx"),   ["header:ab,content:x", "header:ab,content:x"])
    self.assertEqual(test_make_pages_with("abxababx"), ["header:ab,content:x", "header:ab,content:", "header:ab,content:x"])
    self.assertEqual(test_make_pages_with("abxxxx"),   ["header:ab,content:xxxx"])
    listingfile.listing_file_68k.check_page_header = original_check_page_header

def test_remove_undesired_line_breaks_with(page):
  page = create_page_stub(page)
  lines = listingfile.listing_file_68k.remove_undesired_line_breaks(page, 3)
  return list(map(lines_to_string, lines))

class TestFunction_remove_undesired_line_breaks(unittest.TestCase):

  def test_all(self):
    
    self.assertEqual(test_remove_undesired_line_breaks_with(""), [])
    self.assertEqual(test_remove_undesired_line_breaks_with("1"), ["1"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2"), ["1 2"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n3"), ["1 23"])
    page = create_page_stub("")
    self.assertEqual(listingfile.listing_file_68k.remove_undesired_line_breaks(page, 3), [])
    page = create_page_stub("1")
    self.assertEqual(listingfile.listing_file_68k.remove_undesired_line_breaks(page, 3), ["1"])
    page = create_page_stub("1 2")
    self.assertEqual(listingfile.listing_file_68k.remove_undesired_line_breaks(page, 3), ["1 d2"])
    page = create_page_stub("")
    self.assertEqual(listingfile.listing_file_68k.remove_undesired_line_breaks(page, 3), [])
    page = create_page_stub("1 2\n3")
    self.assertEqual(listingfile.listing_file_68k.remove_undesired_line_breaks(page, 3), ["1 23"])