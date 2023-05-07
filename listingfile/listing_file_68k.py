from . import printed_file

import logging
log = logging.getLogger(__name__)

import itertools

def check_page_header(page_no, page, logger = None):
  """ A correct page header looks this way:
JCOBTCC_BIT_Test_Controller                                     28-Apr-2017 14:57:43    XD Ada V1.2A-33                     Page   2
01                                                              28-Apr-2017 14:54:46    JCOBITCP_JCOBTCC.ADA;1                   (1)
"""
  logger = logger if logger else log
  if page == []:
    return True
  if len(page)>61:
    logger.warning("Page {} has too many lines.".format(page_no))
    return False
  if len(page)<2:
    logger.warning("Page {} has no page header.".format(page_no))
    return False
  if (len(str(page[0])) != 132) or (len(str(page[1])) != 132):
    logger.warning("Page {} has an incorrect page header width.".format(page_no))
    return False
  if (str(page[0])[0] == " " or not(str(page[0])[124:].startswith("Page "))):
    logger.warning("Page {} has an incorrect page header line 1.".format(page_no))
    return False
  if (str(page[1])[0] == " " or (str(page[1])[-1] != ")")):
    logger.warning("Page {} has an incorrect page header line 2.".format(page_no))
    return False
  return True

def reconstruct_lost_pages(page_no, lines):
  # The purpose of this function is to reconstruct pages in case the form feed symbols are missing. This is likely
  # to happen when the dos2unix command is used or when the file is changed in a text editor.
  class NoLogging:
    def warning(self):
      pass
  at_first_line = lambda lines, no_of_lines = len(lines) : len(lines) == no_of_lines
  pages = []
  next_page = {"header" : [], "content" : []}
  while True:
    # This is a recursive algorithm. As recursion it is much easyier to understand. But Python does
    # not support recursion. Therefore it must be implemented by a while loop.
    if not(lines):
      return pages + [next_page]
    if check_page_header(page_no, lines, log if at_first_line(lines) else NoLogging):
      if not(at_first_line(lines)):
        log.warning("Reconstructing pages after page {}, which were not introduced by the form feed symbol.".format(page_no))
        pages = pages + [next_page]
      next_page = { "header" : lines[0:2], "content" : [] }
      lines = lines[2:]
    else:
      next_page["content"] = next_page["content"] + [lines[0]]
      lines = lines[1:]
       
class Line:
  def __init__(self, page_no, page_header, page_content, line):
    self.page_no = page_no
    self.page_header = page_header
    self.page_content = page_content
    self.raw = line
  def __add__(self, line):
    return printed_file.MultiText([self, line])
  def __str__(self):
    return str(self.raw)
  def __len__(self):
    return len(self.raw)
  def __getitem__(self, accessor):
    return Line(self.page_no, self.page_header, self.page_content, self.raw[accessor])
  @property
  def lines(self):
    return [self]

def pages_as_lines(pages):
  result = []
  for page_no, page in zip(itertools.count(), pages):
    def make_line(line):
      return Line(page_no, page["header"], page["content"], line) 
    result.extend(list(map(lambda line : make_line(line), page["content"])))
  return result

def remove_undesired_line_breaks(lines, line_length=132):
  # This behaviour is probably incomplete. It is unclear, how line breaks are introduced. We give our best to
  # identify and eliminate them. In case of problems, this function is a source of errors and must be improved.
  # This code is hard to understand. A better more intuitive parsing approach would be be more appropriate.
  # But the code is well tested and works as expected.
  result = []
  lines_before = printed_file.NoText()
  for line in lines:
    if not(str(line)):
      continue
    is_full_line = len(str(line)) == line_length
    is_continuation = lines_before and str(line)[0]!=" "
    if not(lines_before) and not(is_full_line):
      result.append(line)
    elif is_continuation or (not(lines_before)):
      lines_before = lines_before + line
      if not(is_full_line):
        result.append(lines_before)
        lines_before = printed_file.NoText()
    elif lines_before:
      result.append(lines_before)
      lines_before = printed_file.NoText()
      result.append(line)
  if lines_before:
    result.append(lines_before)
  return result
      
def open_file(filename):
  with open(filename, "r") as input:
    pages = printed_file.create_pages_and_lines(input.read())
    all_pages = []
    for page_no, page in zip(itertools.count(), pages):
      form_feeded_pages = reconstruct_lost_pages(page_no, page)
      for page in form_feeded_pages:
        all_pages.append(page)
    all_lines = pages_as_lines(all_pages)
    all_lines = remove_undesired_line_breaks(all_lines)
  return all_lines