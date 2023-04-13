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
  if len(page)>60:
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
  pages = []
  next_page = []
  logger = NoLogging
  while True:
    # This is a recursive algorithm. As recursion it is much easyier to understand. But Python does
    # not support recursion. Therefore it must be a while loop.
    if not(lines):
      return pages + [next_page]
    if check_page_header(page_no, lines, NoLogging):
      logger.warning("Reconstructing pages after page {}, which were not introduced by the form feed symbol.".format(page_no))
      pages = pages + ([next_page] if next_page else [])
      next_page = lines[:2]
      lines = lines[2:]
    else:
      next_page = next_page + [lines[0]]
      lines = lines[1:]
    logger = log
      

def make_pages(page_no, page):
  def make_page(page, with_header = True):
    return {"header" : page[0:2] if with_header else [],
            "content" : page[2:] if with_header else page}
  if page == []:
    return []
  page_header_present = check_page_header(page_no, page)
  all_pages = reconstruct_lost_pages(page_no, page)
  result = [make_page(all_pages[0], page_header_present)]
  result.extend(list(map(lambda page:make_page(page, with_header=True), all_pages[1:])))
  return result

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

def remove_undesired_line_breaks(page_content, line_length=132):
  # This behaviour is probably incomplete. It is unclear, how line breaks are introduced. We give our best to
  # identify and eliminate them. In case of problems, this function is a source of errors and must be improved.
  result = []
  lines_before = []
  for line in page_content + [None]:
    is_line_continuation = (not(lines_before)
             or ( len(lines_before[-1].text())==line_length and line and line.text() and line.text()[0] != " "))
    if is_line_continuation:
      lines_before.append(line)
    else:
      result.append(lines_before)
      lines_before = [line]
  return result
