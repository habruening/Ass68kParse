#!/bin/python3

import unittest
import listingfile.file

import itertools

class TestLogger():
  def __init__(self):
    self.warnings = []
  def warning(self, message):
    self.warnings.append(message)

listingfile.file.log = TestLogger()

class TestClass_Line_Methods(unittest.TestCase):
  def test_all(self):
    line = listingfile.file.Line(17, (4, 8), "0123456789" )
    self.assertEqual(line.text(), "4567")
    self.assertEqual(line.line_no, 17)

class TestFunction_find_first_of(unittest.TestCase):

  def test_normal_operation(self):
    found_at = listingfile.file.find_first_of("abcdefg", ["a"])
    self.assertEqual(found_at, (0,"a"))
    found_at = listingfile.file.find_first_of("abcdefg", ["b"])
    self.assertEqual(found_at, (1,"b"))
    found_at = listingfile.file.find_first_of("abcdefg", ["g"])
    self.assertEqual(found_at, (6,"g"))
    found_at = listingfile.file.find_first_of("abcdefg", ["ab"])
    self.assertEqual(found_at, (0,"ab"))
    found_at = listingfile.file.find_first_of("abcdefg", ["bc"])
    self.assertEqual(found_at, (1,"bc"))
    found_at = listingfile.file.find_first_of("abcdefg", ["fg"])
    self.assertEqual(found_at, (5,"fg"))
    found_at = listingfile.file.find_first_of("abcdefg", ["ab", "a"])
    self.assertEqual(found_at, (0,"ab"))
    found_at = listingfile.file.find_first_of("abcdefg", ["bc", "a"])
    self.assertEqual(found_at, (0,"a"))
    found_at = listingfile.file.find_first_of("abcdefg", ["fg", "a"])
    self.assertEqual(found_at, (0,"a"))
    found_at = listingfile.file.find_first_of("abcdefg", ["a", "b"])
    self.assertEqual(found_at, (0,"a"))
    found_at = listingfile.file.find_first_of("abcdefg", ["b", "c"])
    self.assertEqual(found_at, (1,"b"))
    found_at = listingfile.file.find_first_of("abcdefg", ["g", "f"])
    self.assertEqual(found_at, (5,"f"))
    found_at = listingfile.file.find_first_of("abcdefg", ["ab", "c"])
    self.assertEqual(found_at, (0,"ab"))
    found_at = listingfile.file.find_first_of("abcdefg", ["bc", "d"])
    self.assertEqual(found_at, (1,"bc"))
    found_at = listingfile.file.find_first_of("abcdefg", ["fg", "e"])
    self.assertEqual(found_at, (4,"e"))
    found_at = listingfile.file.find_first_of("abcdefg", ["x", "a"])
    self.assertEqual(found_at, (0,"a"))
    found_at = listingfile.file.find_first_of("abcdefg", ["x", "b"])
    self.assertEqual(found_at, (1,"b"))
    found_at = listingfile.file.find_first_of("abcdefg", ["x", "g"])
    self.assertEqual(found_at, (6,"g"))
    found_at = listingfile.file.find_first_of("abcdefg", ["x", "ab"])
    self.assertEqual(found_at, (0,"ab"))
    found_at = listingfile.file.find_first_of("abcdefg", ["x", "bc"])
    self.assertEqual(found_at, (1,"bc"))
    found_at = listingfile.file.find_first_of("abcdefg", ["x", "fg"])
    self.assertEqual(found_at, (5,"fg"))

  def test_empty_string(self):
    found_at = listingfile.file.find_first_of("", [])
    self.assertFalse(found_at)
    found_at = listingfile.file.find_first_of("", [""])
    self.assertEqual(found_at, (0,""))
    found_at = listingfile.file.find_first_of("", ["x"])
    self.assertFalse(found_at)
    found_at = listingfile.file.find_first_of("", ["x", "y"])
    self.assertFalse(found_at)

  def test_no_values(self):
    found_at = listingfile.file.find_first_of("x", [])
    self.assertFalse(found_at)
    found_at = listingfile.file.find_first_of("x", [""])
    self.assertEqual(found_at, (0,""))

class TestFunction_split_at(unittest.TestCase):

  def test_normal_operation(self):
    elements = listingfile.file.split_at("abcdefg", ["x"])
    self.assertEqual(list(elements), [(0,7)])
    elements = listingfile.file.split_at("abcdefg", ["a"])
    self.assertEqual(list(elements), [(0,0), (1,7)])
    elements = listingfile.file.split_at("abcdefg", ["c"])
    self.assertEqual(list(elements), [(0,2), (3,7)])
    elements = listingfile.file.split_at("abcdefg", ["g"])
    self.assertEqual(list(elements), [(0,6)])
    elements = listingfile.file.split_at("abcdefg", ["a", "d", "g", "x"])
    self.assertEqual(list(elements), [(0,0), (1,3), (4,6)])

  def test_empty_string(self):
    elements = listingfile.file.split_at("", [])
    self.assertFalse(list(elements))
    elements = listingfile.file.split_at("", [""])
    self.assertFalse(list(elements))
    elements = listingfile.file.split_at("", ["", ""])
    self.assertFalse(list(elements))
    elements = listingfile.file.split_at("", ["", "x"])
    self.assertFalse(list(elements))

  def test_warnings(self):
    listingfile.file.log.warnings = []
    found_at = list(listingfile.file.split_at("abcdefg", ["x", "b", "bc"]))
    self.assertFalse(listingfile.file.log.warnings)
    found_at = list(listingfile.file.split_at("abcdefg", ["x", "b", "bc"], ["bc"]))
    self.assertEqual(len(listingfile.file.log.warnings), 1)
    self.assertIn("newline", listingfile.file.log.warnings[0])

class TestFunction_split_pages(unittest.TestCase):

  def test_normal_operation(self):
    pages = listingfile.file.split_pages("x")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("x\fy")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("x\fy\fz")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(next(pages), (4,5))
    self.assertEqual(list(pages), [])

  def test_page_breaks(self):
    pages = listingfile.file.split_pages("x\fy")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("x\f\ry")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (3,4))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("x\f\ny")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (3,4))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("x\f\r\ny")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (4,5))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("x\f\n\ry")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (4,5))
    self.assertEqual(list(pages), [])

  def test_empty_pages(self):
    pages = listingfile.file.split_pages("")
    self.assertEqual(len(list(pages)), 0)
    pages = listingfile.file.split_pages("\f")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("\f\r\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("\f\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("\f\f\f")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("x\f\f\f")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("\fx\f\f")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,2))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("\f\f\fx")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (3,4))
    pages = listingfile.file.split_pages("\f\n\f\n\f\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (4,4))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("x\f\n\f\n\f\n")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(next(pages), (5,5))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("\f\nx\f\n\f\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(next(pages), (5,5))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_pages("\f\n\f\n\f\nx")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (4,4))
    self.assertEqual(next(pages), (6,7))

class TestFunction_split_lines(unittest.TestCase):

  def test_normal_operation(self):
    pages = listingfile.file.split_lines("x")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("x\ny")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("x\ny\nz")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(next(pages), (4,5))
    self.assertEqual(list(pages), [])

  def test_line_breaks(self):
    pages = listingfile.file.split_lines("x\ny")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("x\n\ry")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (3,4))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("x\r\ny")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (3,4))
    self.assertEqual(list(pages), [])

  def test_empty_lines(self):
    pages = listingfile.file.split_lines("")
    self.assertEqual(len(list(pages)), 0)
    pages = listingfile.file.split_lines("\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("\r\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("\n\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("\r\n\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("\n\r\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("\n\n\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(list(pages), [])
    pages = listingfile.file.split_lines("\r\r\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(list(pages), [])

class TestFunction_create_pages_and_lines(unittest.TestCase):
  def test_constructor(self):
    pages = listingfile.file.create_pages_and_lines("\f\n1\n2\f3\f4\f5\f\f6")
    self.assertFalse(pages[0])
    self.assertEqual(pages[1][0].text(), "1")
    self.assertEqual(pages[1][1].text(), "2")
    self.assertEqual(pages[2][0].text(), "3")
    self.assertEqual(pages[3][0].text(), "4")
    self.assertEqual(pages[4][0].text(), "5")
    self.assertFalse(pages[5])
    self.assertEqual(pages[6][0].text(), "6")

  def test_all(self):
    c = ["\f", "\n", "\r", "1", "a", " "]
    for example in map(lambda x : "".join(x), itertools.product(c, c, c, c, c, c, c)):
      pages = listingfile.file.create_pages_and_lines(example)
      line_no = 0
      for page in pages:
        for line in page:
          self.assertEqual(line.line_no, line_no)
          line_no = line_no + 1
          self.assertEqual(example[line.from_to[0]:line.from_to[1]], line.text())
      self.assertEqual("".join(["".join([l.text() for l in p]) for p in pages]),
                       example.replace("\n","").replace("\r", "").replace("\f", ""))
      
  def test_line_numbering(self):
    with open("tests/listingfile/TestData/LineAndPageBreaks.txt", "r") as input, \
         open("tests/listingfile/TestData/LineAndPageBreaks_expected.txt", "r") as expected:
      pages = listingfile.file.create_pages_and_lines(input.read())
      expected = iter(expected.read().splitlines())
      for p in pages:
        for l in p:
          self.assertEqual(next(expected), "{}: {}".format(l.line_no+1, l.text()))
      with self.assertRaises(StopIteration):
        next(expected)

  def test_with_real_file(self):
    with open("tests/listingfile/TestData/JCOBITCP_JCOBTCC.LIS", "r") as input:
      listingfile.file.log.warnings = []
      pages = listingfile.file.create_pages_and_lines(input.read())
      self.assertFalse(listingfile.file.log.warnings)
      for page_no in range(0, 6):
        expected_file_name = "tests/listingfile/TestData/JCOBITCP_JCOBTCC_expected_page_{}.LIS".format(page_no+1)
        with open(expected_file_name, "r") as expected:
          self.assertEqual("\n".join([line.text() for line in pages[page_no]]), expected.read())