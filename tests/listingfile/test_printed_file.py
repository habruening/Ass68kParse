#!/bin/python3

import unittest
import listingfile.printed_file

import itertools

class LoggerStub():
  def __init__(self):
    self.warnings = []
  def warning(self, message):
    self.warnings.append(message)

listingfile.printed_file.log = LoggerStub()

def test_Text_with(file, lines):
  text = listingfile.printed_file.NoText()
  for line in lines:
    text = text + listingfile.printed_file.Text(17, line, file)
  return text

class TestClass_Text_Methods(unittest.TestCase):

  def test_str_operator(self):
    self.assertEqual(str(listingfile.printed_file.Text(0, (0,0), "")), "")
    self.assertEqual(str(listingfile.printed_file.Text(0, (0,0), "0123456789")), "")
    self.assertEqual(str(listingfile.printed_file.Text(0, (0,1), "0123456789")), "0")
    self.assertEqual(str(listingfile.printed_file.Text(0, (0,3), "0123456789")), "012")
    self.assertEqual(str(listingfile.printed_file.Text(0, (3,6), "0123456789")), "345")
    self.assertEqual(str(listingfile.printed_file.Text(0, (6,9), "0123456789")), "678")
    self.assertEqual(str(listingfile.printed_file.Text(0, (9,9), "0123456789")), "")
    self.assertEqual(str(listingfile.printed_file.Text(0, (9,10), "0123456789")), "9")
    self.assertEqual(str(listingfile.printed_file.Text(0, (9,15), "0123456789")), "9")

  def test_len_operator(self):
    self.assertEqual(len(listingfile.printed_file.Text(0, (0,0), "")), 0)
    self.assertEqual(len(listingfile.printed_file.Text(0, (0,0), "0123456789")), 0)
    self.assertEqual(len(listingfile.printed_file.Text(0, (0,1), "0123456789")), 1)
    self.assertEqual(len(listingfile.printed_file.Text(0, (0,3), "0123456789")), 3)
    self.assertEqual(len(listingfile.printed_file.Text(0, (3,6), "0123456789")), 3)
    self.assertEqual(len(listingfile.printed_file.Text(0, (6,9), "0123456789")), 3)
    self.assertEqual(len(listingfile.printed_file.Text(0, (9,9), "0123456789")), 0)
    self.assertEqual(len(listingfile.printed_file.Text(0, (9,10), "0123456789")), 1)
    self.assertEqual(len(listingfile.printed_file.Text(0, (9,15), "0123456789")), 1)

  def test_getitem_operator_element(self):
    text = listingfile.printed_file.Text(0, (0,3), "0123456789")
    self.assertEqual(str(text[0]), "0")
    self.assertEqual(str(text[1]), "1")
    self.assertEqual(str(text[2]), "2")
    self.assertEqual(str(text[-1]), "2")
    self.assertEqual(str(text[-2]), "1")
    self.assertEqual(str(text[-3]), "0")
    text = listingfile.printed_file.Text(0, (7,10), "0123456789")
    self.assertEqual(str(text[0]), "7")
    self.assertEqual(str(text[1]), "8")
    self.assertEqual(str(text[2]), "9")
    self.assertEqual(str(text[-1]), "9")
    self.assertEqual(str(text[-2]), "8")
    self.assertEqual(str(text[-3]), "7")


  def test_getitem_operator_exceptions(self):
    text = listingfile.printed_file.Text(0, (0,0), "")
    with self.assertRaises(IndexError):
      text[0]
    with self.assertRaises(IndexError):
      text[1]
    with self.assertRaises(IndexError):
      text[-1]
    text = listingfile.printed_file.Text(0, (0,0), "0123456789")
    with self.assertRaises(IndexError):
      text[0]
    with self.assertRaises(IndexError):
      text[1]
    with self.assertRaises(IndexError):
      text[-1]
    text = listingfile.printed_file.Text(0, (0,3), "0123456789")
    text[0]
    text[1]
    text[2]
    text[-1]
    text[-2]
    text[-3]
    with self.assertRaises(IndexError):
      text[3]
    with self.assertRaises(IndexError):
      text[-4]
    text = listingfile.printed_file.Text(0, (3,6), "0123456789")
    text[0]
    text[1]
    text[2]
    text[-1]
    text[-2]
    text[-3]
    with self.assertRaises(IndexError):
      text[3]
    with self.assertRaises(IndexError):
      text[-4]

  def test_getitem_operator_slice(self):
    text = listingfile.printed_file.Text(0, (0,3), "0123456789")
    self.assertEqual(str(text[0:3]), "012")
    self.assertEqual(str(text[1:3]), "12")
    self.assertEqual(str(text[0:5]), "012")
    self.assertEqual(str(text[0:-1]), "01")
    self.assertEqual(str(text[0:-2]), "0")
    self.assertEqual(str(text[0:-3]), "")
    self.assertEqual(str(text[0:-4]), "")
    self.assertEqual(str(text[6:10]), "")
    self.assertEqual(str(text[6:-4]), "")
    self.assertEqual(str(text[0:-10]), "")
    self.assertEqual(str(text[0:10]), "012")
    self.assertEqual(str(text[-10:2]), "01")
    self.assertEqual(str(text[-2:-1]), "1")
    self.assertEqual(str(text[-1:-2]), "")

class TestClass_MultiText_Methods(unittest.TestCase):
  def test_all(self):
    line = listingfile.printed_file.Text(17, (4, 8), "0123456789" )
    self.assertEqual(str(line), "4567")
    self.assertEqual(line.line_no, 17)

  def test_str_operator(self):
    self.assertEqual(str(test_Text_with("", [(0,0)])), "")
    self.assertEqual(str(test_Text_with("", [(0,1)])), "")
    self.assertEqual(str(test_Text_with("x", [(0,0)])), "")
    self.assertEqual(str(test_Text_with("x", [(0,1)])), "x")
    self.assertEqual(str(test_Text_with("x", [(3,5)])), "")
    self.assertEqual(str(test_Text_with("abcdefghij", [(0,1)])), "a")
    self.assertEqual(str(test_Text_with("abcdefghij", [(0,2)])), "ab")
    self.assertEqual(str(test_Text_with("abcdefghij", [(2,4)])), "cd")
    self.assertEqual(str(test_Text_with("abcdefghij", [(4,8)])), "efgh")
    self.assertEqual(str(test_Text_with("abcdefghij", [(0,3), (4,6)])), "abcef")
    self.assertEqual(str(test_Text_with("abcdefghij", [(0,1), (2,3), (6,7), (9,10), (4,5)])), "acgje")

  def test_len_operator(self):
    self.assertEqual(len(test_Text_with("", [(0,0)])), 0)
    self.assertEqual(len(test_Text_with("", [(0,1)])), 0)
    self.assertEqual(len(test_Text_with("x", [(0,0)])), 0)
    self.assertEqual(len(test_Text_with("x", [(0,1)])), 1)
    self.assertEqual(len(test_Text_with("x", [(3,5)])), 0)
    self.assertEqual(len(test_Text_with("abcdefghij", [(0,1)])), 1)
    self.assertEqual(len(test_Text_with("abcdefghij", [(0,2)])), 2)
    self.assertEqual(len(test_Text_with("abcdefghij", [(2,4)])), 2)
    self.assertEqual(len(test_Text_with("abcdefghij", [(4,8)])), 4)
    self.assertEqual(len(test_Text_with("abcdefghij", [(0,3), (4,6)])), 5)
    self.assertEqual(len(test_Text_with("abcdefghij", [(0,1), (2,3), (6,7), (9,10), (4,5)])), 5)

  def test_getitem_operator_element(self):
    text = test_Text_with("0123456789", [(0,1), (1,3)])
    self.assertEqual(str(text[0]), "0")
    self.assertEqual(str(text[1]), "1")
    self.assertEqual(str(text[2]), "2")
    self.assertEqual(str(text[-1]), "2")
    self.assertEqual(str(text[-2]), "1")
    self.assertEqual(str(text[-3]), "0")
    text = test_Text_with("0123456789", [(7,9), (9,10)])
    self.assertEqual(str(text[0]), "7")
    self.assertEqual(str(text[1]), "8")
    self.assertEqual(str(text[2]), "9")
    self.assertEqual(str(text[-1]), "9")
    self.assertEqual(str(text[-2]), "8")
    self.assertEqual(str(text[-3]), "7")


  def test_getitem_operator_exceptions(self):
    text = test_Text_with("", [(0,0), (0,0)])
    with self.assertRaises(IndexError):
      text[0]
    with self.assertRaises(IndexError):
      text[1]
    with self.assertRaises(IndexError):
      text[-1]
    text = test_Text_with("0123456789", [(0,0), (0,0)])
    with self.assertRaises(IndexError):
      text[0]
    with self.assertRaises(IndexError):
      text[1]
    with self.assertRaises(IndexError):
      text[-1]
    text = test_Text_with("0123456789", [(0,1), (1,3)])
    text[0]
    text[1]
    text[2]
    text[-1]
    text[-2]
    text[-3]
    with self.assertRaises(IndexError):
      text[3]
    with self.assertRaises(IndexError):
      text[-4]
    text = test_Text_with("0123456789", [(3,4), (4,5), (5,6)])
    text[0]
    text[1]
    text[2]
    text[-1]
    text[-2]
    text[-3]
    with self.assertRaises(IndexError):
      text[3]
    with self.assertRaises(IndexError):
      text[-4]

  def test_getitem_operator_slice(self):
    text = test_Text_with("0123456789", [(0,1), (1,3)])
    self.assertEqual(str(text[0:3]), "012")
    self.assertEqual(str(text[1:3]), "12")
    self.assertEqual(str(text[0:5]), "012")
    self.assertEqual(str(text[0:-1]), "01")
    self.assertEqual(str(text[0:-2]), "0")
    self.assertFalse(text[0:-3])
    self.assertFalse(text[0:-4])
    self.assertFalse(text[6:10])
    self.assertFalse(text[6:-4])
    self.assertFalse(text[0:-10])
    self.assertEqual(str(text[0:10]), "012")
    self.assertEqual(str(text[-10:2]), "01")
    self.assertEqual(str(text[-2:-1]), "1")
    self.assertFalse(text[-1:-2])
    text = test_Text_with("0123456789ABCDEFGHIKLM", [(0,4), (4,8), (8,12)])
    self.assertEqual(str(text[5:10]), "56789")


class TestFunction_find_first_of(unittest.TestCase):

  # find_first_of(..., [""]) is not foreseen and therefore not tested. There would be no
  # error reporting and no exception been raised.

  def test_normal_operation(self):
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["a"])
    self.assertEqual(found_at, (0,"a"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["b"])
    self.assertEqual(found_at, (1,"b"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["g"])
    self.assertEqual(found_at, (6,"g"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["ab"])
    self.assertEqual(found_at, (0,"ab"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["bc"])
    self.assertEqual(found_at, (1,"bc"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["fg"])
    self.assertEqual(found_at, (5,"fg"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["ab", "a"])
    self.assertEqual(found_at, (0,"ab"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["bc", "a"])
    self.assertEqual(found_at, (0,"a"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["fg", "a"])
    self.assertEqual(found_at, (0,"a"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["a", "b"])
    self.assertEqual(found_at, (0,"a"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["b", "c"])
    self.assertEqual(found_at, (1,"b"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["g", "f"])
    self.assertEqual(found_at, (5,"f"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["ab", "c"])
    self.assertEqual(found_at, (0,"ab"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["bc", "d"])
    self.assertEqual(found_at, (1,"bc"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["fg", "e"])
    self.assertEqual(found_at, (4,"e"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["x", "a"])
    self.assertEqual(found_at, (0,"a"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["x", "b"])
    self.assertEqual(found_at, (1,"b"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["x", "g"])
    self.assertEqual(found_at, (6,"g"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["x", "ab"])
    self.assertEqual(found_at, (0,"ab"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["x", "bc"])
    self.assertEqual(found_at, (1,"bc"))
    found_at = listingfile.printed_file.find_first_of("abcdefg", ["x", "fg"])
    self.assertEqual(found_at, (5,"fg"))

  def test_empty_string(self):
    found_at = listingfile.printed_file.find_first_of("", [])
    self.assertFalse(found_at)
    found_at = listingfile.printed_file.find_first_of("", [""])
    self.assertEqual(found_at, (0,""))
    found_at = listingfile.printed_file.find_first_of("", ["x"])
    self.assertFalse(found_at)
    found_at = listingfile.printed_file.find_first_of("", ["x", "y"])
    self.assertFalse(found_at)

  def test_no_values(self):
    found_at = listingfile.printed_file.find_first_of("x", [])
    self.assertFalse(found_at)
    found_at = listingfile.printed_file.find_first_of("x", [""])
    self.assertEqual(found_at, (0,""))

class TestFunction_split_at(unittest.TestCase):

  # split_at(..., [""]) is not foreseen and therefore not tested. There would be no
  # error reporting and no exception been raised. It would result in an endless loop.
  # Defensive programming is not needed. The caller must ensure that the function is
  # called correctly.

  def test_normal_operation(self):
    elements = listingfile.printed_file.split_at("abcdefg", ["x"])
    self.assertEqual(list(elements), [(0,7)])
    elements = listingfile.printed_file.split_at("abcdefg", ["a"])
    self.assertEqual(list(elements), [(0,0), (1,7)])
    elements = listingfile.printed_file.split_at("abcdefg", ["c"])
    self.assertEqual(list(elements), [(0,2), (3,7)])
    elements = listingfile.printed_file.split_at("abcdefg", ["g"])
    self.assertEqual(list(elements), [(0,6), (7,7)])
    elements = listingfile.printed_file.split_at("abcdefg", ["a", "d", "g", "x"])
    self.assertEqual(list(elements), [(0,0), (1,3), (4,6), (7,7)])

  def test_empty_string(self):
    elements = listingfile.printed_file.split_at("", [])
    self.assertEqual(list(elements), [(0,0)])
    elements = listingfile.printed_file.split_at("", ["x"])
    self.assertEqual(list(elements), [(0,0)])

  def test_warnings(self):
    listingfile.printed_file.log.warnings = []
    found_at = list(listingfile.printed_file.split_at("abcdefg", ["x", "b", "bc"]))
    self.assertFalse(listingfile.printed_file.log.warnings)
    found_at = list(listingfile.printed_file.split_at("abcdefg", ["x", "b", "bc"], ["bc"]))
    self.assertEqual(len(listingfile.printed_file.log.warnings), 1)
    self.assertIn("newline", listingfile.printed_file.log.warnings[0])

class TestFunction_split_pages(unittest.TestCase):

  def test_normal_operation(self):
    pages = listingfile.printed_file.split_pages("x")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("x\fy")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("x\fy\fz")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(next(pages), (4,5))
    self.assertEqual(list(pages), [])

  def test_page_breaks(self):
    pages = listingfile.printed_file.split_pages("x\fy")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("x\f\ry")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (3,4))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("x\f\ny")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (3,4))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("x\f\r\ny")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (4,5))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("x\f\n\ry")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (4,5))
    self.assertEqual(list(pages), [])

  def test_empty_pages(self):
    pages = listingfile.printed_file.split_pages("")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(len(list(pages)), 0)
    pages = listingfile.printed_file.split_pages("\f")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("\f\r\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("\f\r\nx")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (3,4))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("\f\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("\f\f\f")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("x\f\f\f")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(next(pages), (4,4))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("\fx\f\f")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,2))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(next(pages), (4,4))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("\f\f\fx")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (3,4))
    pages = listingfile.printed_file.split_pages("\f\n\f\n\f\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (4,4))
    self.assertEqual(next(pages), (6,6))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("x\f\n\f\n\f\n")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(next(pages), (5,5))
    self.assertEqual(next(pages), (7,7))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("\f\nx\f\n\f\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(next(pages), (5,5))
    self.assertEqual(next(pages), (7,7))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_pages("\f\n\f\n\f\nx")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (4,4))
    self.assertEqual(next(pages), (6,7))
    pages = listingfile.printed_file.split_pages("\f\n\f\n\f\r\n\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (4,4))
    self.assertEqual(next(pages), (7,8))

class TestFunction_split_lines(unittest.TestCase):

  def test_normal_operation(self):
    pages = listingfile.printed_file.split_lines("x")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("x\ny")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("x\ny\nz")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(next(pages), (4,5))
    self.assertEqual(list(pages), [])


  def test_line_breaks(self):
    pages = listingfile.printed_file.split_lines("x\ny")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("x\n\ry")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (3,4))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("x\r\ny")
    self.assertEqual(next(pages), (0,1))
    self.assertEqual(next(pages), (3,4))
    self.assertEqual(list(pages), [])

  def test_empty_lines(self):
    pages = listingfile.printed_file.split_lines("")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(len(list(pages)), 0)
    pages = listingfile.printed_file.split_lines("\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("\r\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("\n\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("\r\n\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("\n\r\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("\n\n\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("\r\r\n")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (1,1))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(list(pages), [])
    pages = listingfile.printed_file.split_lines("\r\n\r")
    self.assertEqual(next(pages), (0,0))
    self.assertEqual(next(pages), (2,2))
    self.assertEqual(next(pages), (3,3))
    self.assertEqual(list(pages), [])

class TestFunction_create_pages_and_lines(unittest.TestCase):
  def test_constructor(self):
    pages = listingfile.printed_file.create_pages_and_lines("\f\n1\n2\f3\f4\f5\f\f6")
    self.assertEqual(str(pages[0][0]), "")
    self.assertEqual(str(pages[1][0]), "1")
    self.assertEqual(str(pages[1][1]), "2")
    self.assertEqual(str(pages[2][0]), "3")
    self.assertEqual(str(pages[3][0]), "4")
    self.assertEqual(str(pages[4][0]), "5")
    self.assertEqual(str(pages[5][0]), "")
    self.assertEqual(str(pages[6][0]), "6")

  def test_all(self):
    c = ["\f", "\n", "\r", "1", "a", " "]
    for example in map(lambda x : "".join(x), itertools.product(c, c, c, c, c, c, c)):
      pages = listingfile.printed_file.create_pages_and_lines(example)
      line_no = 0
      for page in pages:
        for line in page:
          self.assertEqual(line.line_no, line_no)
          line_no = line_no + 1
          self.assertEqual(example[line.from_to[0]:line.from_to[1]], str(line))
      self.assertEqual("".join(["".join([str(l) for l in p]) for p in pages]),
                       example.replace("\n","").replace("\r", "").replace("\f", ""))
    
  def test_line_numbering(self):
    with open("tests/listingfile/TestData/LineAndPageBreaks.txt", "r") as input, \
         open("tests/listingfile/TestData/LineAndPageBreaks_expected.txt", "r") as expected:
      pages = listingfile.printed_file.create_pages_and_lines(input.read())
      expected = iter(expected.read().splitlines())
      for p in pages:
        for l in p:
          self.assertEqual(next(expected), "{}: {}".format(l.line_no+1, str(l)))
      with self.assertRaises(StopIteration):
        next(expected)

  def test_empty_page(self):
    """       0 1 2 3       4 5 6         7 8 9 10
             \f\r\n x      \f\r\n        \f\r\n x
       [0][0]       [1][0]        [2][0]        [3][0]"""
    pages = listingfile.printed_file.create_pages_and_lines("\f\r\nx\f\r\n\f\r\nx")
    self.assertEqual(pages[0][0].from_to, (0,0))
    self.assertEqual(pages[0][0].line_no, 0)
    self.assertEqual(pages[1][0].from_to, (3,4))
    self.assertEqual(pages[1][0].line_no, 1)
    self.assertEqual(pages[2][0].from_to, (7,7))
    self.assertEqual(pages[2][0].line_no, 2)
    self.assertEqual(pages[3][0].from_to, (10,11))
    self.assertEqual(pages[3][0].line_no, 3)

  def test_with_real_file(self):
    self.maxDiff = 2000
    with open("tests/listingfile/TestData/JCOBITCP_JCOBTCC.LIS", "r") as input:
      listingfile.printed_file.log.warnings = []
      pages = listingfile.printed_file.create_pages_and_lines(input.read())
      self.assertFalse(listingfile.printed_file.log.warnings)
      for page_no in range(0, 7):
        expected_file_name = "tests/listingfile/TestData/JCOBITCP_JCOBTCC_expected_page_{}.LIS".format(page_no+1)
        with open(expected_file_name, "r") as expected:
          self.assertEqual("\n".join([str(line) for line in pages[page_no]]), expected.read())
