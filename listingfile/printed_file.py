#!/bin/python3

import logging
log = logging.getLogger(__name__)

import itertools

class Line:
  def __init__(self, line_no, from_to, file):
    self.line_no = line_no  # The line number is not checked.
    self.from_to = from_to
    self.file = file
  def text(self):
    return self.file[self.from_to[0]:self.from_to[1]]

def find_first_of(text, values): 
  best_match = False
  for value in values:
    if 0 <= (found_at := text.find(value)):
      if(not best_match or found_at < best_match[0] 
                        or (found_at == best_match[0] and len(best_match[1]) < len(value))):
        best_match = (found_at, value)
  return best_match

def split_at(file, separators, warn_if_separator = []):
  position = 0
  while (position < len(file)):
    if page_break_at := find_first_of(file[position:], separators):
      if page_break_at[1] in warn_if_separator:
        log.warning("There are incorrect newline encodings. Line numbers will be incorrect.")
      yield (position, position + page_break_at[0])
      position = position + page_break_at[0] + len(page_break_at[1])
    else:
      yield (position, len(file))
      position = len(file)

def split_pages(file):
  yield from split_at(file, ["\f\r\n", "\f\n\r", "\f\n", "\f\r", "\f"], ["\f"])

def split_lines(file):
  yield from split_at(file, ["\r\n", "\n\r", "\n", "\r"], ["\n\r"])

def create_pages_and_lines(file):
  result = []
  line_no = 0
  for page in split_pages(file):
    new_page = []
    for line in split_lines(file[page[0]:page[1]]):
      line = Line(line_no, (page[0]+line[0], page[0]+line[1]), file)
      line_no = line_no + 1
      new_page.append(line)
    result.append(new_page)
  return result
    
