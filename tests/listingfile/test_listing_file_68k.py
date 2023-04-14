#!/bin/python3

import unittest
import listingfile.listing_file_68k

import itertools

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
      test = header + "\n" + "\n".join([str(i) for i in range(1,60)])
      listingfile.listing_file_68k.log.warnings = []
      header_correct = listingfile.listing_file_68k.check_page_header(1, create_page_stub(test))
      self.assertTrue(header_correct)
      self.assertFalse(listingfile.listing_file_68k.log.warnings)
      test = test + "\n" + "60"
      header_correct = listingfile.listing_file_68k.check_page_header(1, create_page_stub(test))
      self.assertFalse(header_correct)
      self.assertIn("too many lines", listingfile.listing_file_68k.log.warnings[0])
         

def check_page_header_stub(page_no, page, logger = False):
  if len(page)<2:
    return False
  if (page[0].text() != "a") or (not(page[1].text() in ["b", "c"])):
    return False
  return True
  
def test_reconstruct_lost_pages_with(text):
  pages = listingfile.listing_file_68k.reconstruct_lost_pages(17, [LineStub(l) for l in text])
  return [":".join(["".join([l.text() for l in v]) for v in p.values()]) for p in pages]

class TestFunction_reconstruct_lost_pages(unittest.TestCase):

  def test_examples(self):
    original_check_page_header = listingfile.listing_file_68k.check_page_header
    listingfile.listing_file_68k.check_page_header = check_page_header_stub
    self.assertEqual(test_reconstruct_lost_pages_with(""), [":"])
    self.assertEqual(test_reconstruct_lost_pages_with("x"), [":x"])
    self.assertEqual(test_reconstruct_lost_pages_with("xab"), [":x", "ab:"])
    self.assertEqual(test_reconstruct_lost_pages_with("a"), [":a"])
    self.assertEqual(test_reconstruct_lost_pages_with("ab"), ["ab:"])
    self.assertEqual(test_reconstruct_lost_pages_with("aba"), ["ab:a"])
    self.assertEqual(test_reconstruct_lost_pages_with("abab"), ["ab:", "ab:"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxab"), ["ab:x", "ab:"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxabx"), ["ab:x", "ab:x"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxababx"), ["ab:x", "ab:", "ab:x"])
    self.assertEqual(test_reconstruct_lost_pages_with("abac"), ["ab:", "ac:"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxac"), ["ab:x", "ac:"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxacx"), ["ab:x", "ac:x"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxacabx"), ["ab:x", "ac:", "ab:x"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxabacx"), ["ab:x", "ab:", "ac:x"])
    self.assertEqual(test_reconstruct_lost_pages_with("abxacacx"), ["ab:x", "ac:", "ac:x"])
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

def test_remove_undesired_line_breaks_with(page):
  page = create_page_stub(page)
  lines = listingfile.listing_file_68k.remove_undesired_line_breaks(page, 3)
  return list(map(lines_to_string, lines))

class TestFunction_remove_undesired_line_breaks(unittest.TestCase):

  def test_all(self):
    self.assertEqual(test_remove_undesired_line_breaks_with(""), [])
    self.assertEqual(test_remove_undesired_line_breaks_with("\n"), [""])
    self.assertEqual(test_remove_undesired_line_breaks_with("\n\n"), ["", ""])
    self.assertEqual(test_remove_undesired_line_breaks_with("1\n\n"), ["1", ""])
    self.assertEqual(test_remove_undesired_line_breaks_with("\n1\n"), ["", "1"])
    self.assertEqual(test_remove_undesired_line_breaks_with("\n\n1"), ["", "", "1"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1"), ["1"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2"), ["1 2"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n 3"), ["1 2", " 3"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n3"), ["1 23"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1  \n2"), ["1  2"])
    self.assertEqual(test_remove_undesired_line_breaks_with(" \n1"), [" ", "1"])
    self.assertEqual(test_remove_undesired_line_breaks_with("  \n1"), ["  ", "1"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2 "), ["1 2 "])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2 \n 3"), ["1 2 ", " 3"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2 \n3"), ["1 2 ", "3"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1   \n2"), ["1   ", "2"])
    self.assertEqual(test_remove_undesired_line_breaks_with(" \n1"), [" ", "1"])
    self.assertEqual(test_remove_undesired_line_breaks_with("  \n1"), ["  ", "1"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n3 4\n5"), ["1 23 45"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n3 4\n5 6"), ["1 23 45 6"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n3 4\n5 6\n 7"), ["1 23 45 6", " 7"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n3 4\n "), ["1 23 4", " "])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n3 4\n5\n"), ["1 23 45"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n3 4\n5 6\n"), ["1 23 45 6"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n3 4\n5 6\n 7\n"), ["1 23 45 6", " 7"])
    self.assertEqual(test_remove_undesired_line_breaks_with("1 2\n3 4\n \n"), ["1 23 4", " "])

def test_pages_as_lines_with(headers, pages):
  lines = listingfile.listing_file_68k.pages_as_lines(
    map(lambda header, page : {"header" : header,
                                    "content" : list(map(lambda line : LineStub(line), page))},
                    headers, pages))
  return ["{}:{}:{}".format(line.page_no,line.page_header,line.content.text()) for line in lines]

class Testpages_as_lines(unittest.TestCase):

  def test_all(self):
    self.assertEqual(test_pages_as_lines_with([],[]),
                     [])
    self.assertEqual(test_pages_as_lines_with(["page_1"],[]),             
                     [])
    self.assertEqual(test_pages_as_lines_with(["page_1"],[["line_1"]]),
                     ["0:page_1:line_1"])
    self.assertEqual(test_pages_as_lines_with([""], [["line_1"]]),  
                     ["0::line_1"])
    self.assertEqual(test_pages_as_lines_with(["page_1"], [["line_1", "line_2"]]),   
                     ["0:page_1:line_1", "0:page_1:line_2"])
    self.assertEqual(test_pages_as_lines_with(["page_1"], [["", "line_2"]]),   
                     ["0:page_1:", "0:page_1:line_2"])
    self.assertEqual(test_pages_as_lines_with(["page_1"], [["line_1", ""]]),   
                     ["0:page_1:line_1", "0:page_1:"])
    self.assertEqual(test_pages_as_lines_with(["page_1", "page_2"], [["line_1", "line_2"], []]),   
                     ["0:page_1:line_1", "0:page_1:line_2"])
    self.assertEqual(test_pages_as_lines_with(["page_1", "page_2"], [["line_1", "line_2"], ["line_3"]]),   
                     ["0:page_1:line_1", "0:page_1:line_2", "1:page_2:line_3"])
    self.assertEqual(test_pages_as_lines_with(["page_1", "page_2"], [["line_1", "line_2"], ["line_3", "line_4"]]),   
                     ["0:page_1:line_1", "0:page_1:line_2", "1:page_2:line_3", "1:page_2:line_4"])
    self.assertEqual(test_pages_as_lines_with(["page_1", "page_2"], [["line_1", "line_2"], ["line_3", ""]]),   
                     ["0:page_1:line_1", "0:page_1:line_2", "1:page_2:line_3", "1:page_2:"])
    self.assertEqual(test_pages_as_lines_with(["page_1", "page_2"], [[], ["line_1"]]),   
                     ["1:page_2:line_1"])
    self.assertEqual(test_pages_as_lines_with(["page_1", "page_2"], [["line_1"], []]),   
                     ["0:page_1:line_1"])
    
class SAT_Tests(unittest.TestCase):

  def test_with_real_file(self):

    with open("tests/listingfile/TestData/JCOBITCP_JCOBTCC.LIS", "r") as input, \
         open("tests/listingfile/TestData/JCOBITCP_JCOBTCC_expected_line_numbers.LIS") as expected_lines:
      expected_lines = iter(expected_lines.read().splitlines())
      listingfile.printed_file.log.warnings = []
      pages = listingfile.printed_file.create_pages_and_lines(input.read())
      all_pages = []
      for page_no, page in zip(itertools.count(), pages):
        form_feeded_pages = listingfile.listing_file_68k.reconstruct_lost_pages(page_no, page)
        for page in form_feeded_pages:
          for line in page["content"]:
            self.assertEqual(next(expected_lines), "{}:{}".format(line.line_no+1,line.text()))
      #listingfile.listing_file_68k.pages_as_lines(pages)
      #  #all_pages.extend(listingfile.listing_file_68k.make_pages(page_no, page))
      #lines = listingfile.listing_file_68k.pages_as_lines(all_pages)
      #for line in lines:
        #print("Header:")
        #print(listingfile.printed_file.lines_text(line.page_header))
        #print("Line:")
        #print(line.text())
      #  self.assertEqual(expected_lines[line.content.line_no], line.text())
      #lines = listingfile.listing_file_68k.remove_undesired_line_breaks(lines)
      #for line in lines:
      #  print(lines_to_string(line))
