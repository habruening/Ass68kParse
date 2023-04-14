from . import printed_file

import logging
log = logging.getLogger(__name__)

import itertools

def check_page_header(page_no, page, logger = log):
  """ A correct page header looks this way:
JCOBTCC_BIT_Test_Controller                                     28-Apr-2017 14:57:43    XD Ada V1.2A-33                     Page   2
01                                                              28-Apr-2017 14:54:46    JCOBITCP_JCOBTCC.ADA;1                   (1)
"""
  if page == []:
    return True
  if len(page)>61:
    log.warning("Page {} has too many lines.".format(page_no))
    return False
  if len(page)<2:
    log.warning("Page {} has no page header.".format(page_no))
    return False
  if (len(page[0].text()) != 132) or (len(page[1].text()) != 132):
    log.warning("Page {} has an incorrect page header width.".format(page_no))
    return False
  if (page[0].text()[0] == " " or not(page[0].text()[124:].startswith("Page "))):
    log.warning("Page {} has an incorrect page header line 1.".format(page_no))
    return False
  if (page[1].text()[0] == " " or (page[1].text()[-1] != ")")):
    log.warning("Page {} has an incorrect page header line 2.".format(page_no))
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
  def __init__(self, page_no, page_header, line):
    self.page_no = page_no
    self.page_header = page_header
    self.content = line
  def text(self):
    return self.content.text()

def pages_as_lines(pages):
  result = []
  for page_no, page in zip(itertools.count(), pages):
    result.extend(list(map(lambda line : Line(page_no, page["header"], line), page["content"])))
  return result

def remove_undesired_line_breaks(lines, line_length=132):
  # This behaviour is probably incomplete. It is unclear, how line breaks are introduced. We give our best to
  # identify and eliminate them. In case of problems, this function is a source of errors and must be improved.
  result = []
  lines_before = []
  for line in lines + [None]:
    is_full_line = line and line.text() and len(line.text()) == line_length
    is_continuation = line and line.text() and line.text()[0]!=" "
    if line and not(lines_before) and not(is_full_line):
      result.append([line])
    elif not(lines_before) and is_full_line:
      lines_before.append(line)
    elif lines_before and is_continuation and not(is_full_line):
      result.append(lines_before + [line])
      lines_before = []
    elif lines_before and is_continuation and is_full_line:
      lines_before.append(line)
    elif lines_before and not(is_continuation) and line and line.text():
      result.append(lines_before)
      result.append([line])
      lines_before = []
    elif line == None and lines_before:
      result.append(lines_before)
  return result
      
