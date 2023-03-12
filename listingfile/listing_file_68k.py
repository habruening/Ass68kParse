from . import printed_file

import logging
log = logging.getLogger(__name__)

def check_page_header(page_no, page):
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