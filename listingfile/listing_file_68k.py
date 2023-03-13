from . import printed_file

import logging
log = logging.getLogger(__name__)

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

def reconstruct_lost_pages(page_no, page):
  # The purpose of this function is to reconstruct pages in case the form feed symbols are missing. This is likely
  # to happen when the dos2unix command is used or when the file is changed in a text editor.
  reconstructed_pages = []
  page_start = 0
  class NoLogging:
    def warning(self):
      pass
  for line in range(1,len(page)+1):
    if (line == len(page)) or check_page_header(page_no, page[line:], NoLogging()):
      reconstructed_pages.append(page[page_start:line])
      if 0 < page_start:
        log.warning("Reconstructing pages after page {}, which were not introduced by the form feed symbol.".format(page_no))
      page_start = line
  return reconstructed_pages  