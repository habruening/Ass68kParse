import logging
log = logging.getLogger(__name__)

# The purpose of these functions is to read a file that is arranged as pages.
#
# The pages are separated with the form feed symbol '\r', 0x0c. The lines are separated by line
# feed symbol ('\n', 0x0A), by the carriage return ('\r', 0x0D) or by a combination of both.
# 
# The motivation for these functions is that in the later processing we always want to keep the
# information where in the original file (e.g. the line numbers) we are. For example when correcting
# line breaks, we want to ensure, that we at any time know what was the original. This is important
# for good status and error messages and also for GUI applications that show us the original file.

class NoText:
  def __add__(self, text):
    return text
  def __bool__(self):
    return False
  
def make_valid_text_access(text, accessor):
  if type(accessor) == int:
    if (accessor < -len(text)) or (len(text) <= accessor): 
      raise IndexError
    if accessor < 0:
      accessor = len(text) + accessor
    return (accessor, accessor+1)
  if type(accessor)==slice:
    if accessor.step:
      raise IndexError
    accessor_start, accessor_stop = accessor.start, accessor.stop
    if accessor_start < 0:
      accessor_start = len(text) + accessor_start
    accessor_start = max(accessor_start, 0)
    accessor_start = min(accessor_start, len(text))
    if accessor_stop < 0:
      accessor_stop = len(text) + accessor_stop
    accessor_stop = max(accessor_stop, 0)
    accessor_stop = min(accessor_stop, len(text))
    return (accessor_start, accessor_stop)
  raise IndexError
     
class Text:
  def __init__(self, line_no, from_to, file):
    self.line_no = line_no  # The line number is not checked.
    self.from_to = tuple(map(lambda x : min(len(file), x), from_to))
    self.file = file
  def __add__(self, text):
    return MultiText([self, text])
  def __str__(self):
    return self.file[self.from_to[0]:self.from_to[1]]
  def __len__(self):
    return self.from_to[1] - self.from_to[0]
  def __getitem__(self, accessor):
    valid_access = make_valid_text_access(self, accessor)
    valid_access = (valid_access[0] + self.from_to[0], valid_access[1] + self.from_to[0])
    return Text(self.line_no, valid_access, self.file)

class MultiText:
  def __init__(self, lines):
    self.lines = lines
  def __add__(self, text):
    return MultiText(self.lines + [text])
  def __str__(self):
    return "".join([str(line) for line in self.lines])
  def __len__(self):
    return sum([len(line) for line in self.lines])
  def __getitem__(self, accessor):
    valid_access = make_valid_text_access(self, accessor)
    result = NoText()
    for line in self.lines:
      if valid_access[0] < len(line) and valid_access[0] < valid_access[1]:
        snip = (valid_access[0], min(len(line), valid_access[1]))
        result = result + line[valid_access[0]:valid_access[1]]
        valid_access = (0, valid_access[1] - snip[1] - snip[0])
      else:
        valid_access = (valid_access[0] - len(line), valid_access[1] - len(line))
    return result
      
def find_first_of(text, values):
  """find_first_of cannot be be called with "" in values """
  best_match = False
  for value in values:
    if 0 <= (found_at := text.find(value)):
      if(not best_match or found_at < best_match[0] 
                        or (found_at == best_match[0] and len(best_match[1]) < len(value))):
        best_match = (found_at, value)
  return best_match

def split_at(file, separators, warn_if_separator = []):
  """find_first_of cannot be be called with "" in separators """
  """If this function is called inco"""
  position = 0
  while (True):
    if found_at := find_first_of(file[position:], separators):
      if found_at[1] in warn_if_separator:
        log.warning("There are incorrect newline encodings. Line numbers may be incorrect.")
      yield (position, position + found_at[0])
      position = position + found_at[0] + len(found_at[1])
    else:
      yield (position, len(file))
      break

def split_pages(file):
  yield from split_at(file, ["\f\r\n", "\f\n\r", "\f\n", "\f\r", "\f"], ["\f"])

def split_lines(file):
  yield from split_at(file, ["\r\n", "\n", "\r"])

def create_pages_and_lines(file):
  result = []
  line_no = 0
  for page in split_pages(file):
    new_page = []
    for line in split_lines(file[page[0]:page[1]]):
      line = Text(line_no, (page[0]+line[0], page[0]+line[1]), file)
      line_no = line_no + 1
      new_page.append(line)
    result.append(new_page)
  return result
    
