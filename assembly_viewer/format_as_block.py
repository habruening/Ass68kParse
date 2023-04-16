
# These functions are needed, because the TextView does not support colored lines.
# We must reformat the text to a block.
# Todo: Ask on StackOverflow for an alternative.

class Translator():

  def create_mapping(source, target):
    return {"source" : source, "target" : target}
  
  def __init__(self):
    self.mapping = [Translator.create_mapping(0, 0)]

  def add_mapping(self, source, target):
    self.mapping.append(Translator.create_mapping(self.mapping[-1]["source"] + source, self.mapping[-1]["target"] + target))

  def add_mappings(self, translator):
    mappings = [Translator.create_mapping(mapping["source"] + self.mapping[-1]["source"],
                                          mapping["target"] + self.mapping[-1]["target"]) for mapping in translator.mapping]
    self.mapping.extend(mappings[1:])

  def source_to_target(self, source):
    i = 0
    while (i < len(self.mapping)) and self.mapping[i]["source"] <= source:
      i = i + 1
    return self.mapping[i-1]["target"] + source - self.mapping[i-1]["source"]

  def target_to_source(self, target):
    i = 0
    while self.mapping[i]["target"] <= target:
      i = i + 1
    source = self.mapping[i-1]["source"] + target - self.mapping[i-1]["target"]
    return source if source < self.mapping[i]["source"] else self.mapping[i]["source"]

def adjust_line_length(line, line_length, tab_size = 8):
  translations = Translator()
  line_text = line.rstrip("\n\r\f")
  line_ending = line[len(line_text):]
  tab_parts = line_text.split("\t")
  line_text = tab_parts[0]
  translations.add_mapping(len(tab_parts[0]), len(tab_parts[0]))
  for tab_part in tab_parts[1:]:
    tab_spaces = " " * (tab_size - (len(line_text) % tab_size))
    line_text = line_text + tab_spaces
    line_text = line_text + tab_part
    translations.add_mapping(len(tab_part) + 1, len(tab_part) + len(tab_spaces))
  extra_spaces = max(line_length - len(line_text),0)
  new_line = line_text + " " * extra_spaces + line_ending
  translations.add_mapping(len(line_ending), extra_spaces + len(line_ending))
  return new_line, translations

def adjust_line_lengths(text, line_length, tab_size = 8):
  translations = Translator()
  result = ""
  for line in text.splitlines(keepends=True):
    new_line, line_translations = adjust_line_length(line, line_length, tab_size)
    translations.add_mappings(line_translations)
    result = result + new_line
  return {"text" : result, "translator" : translations}

class TextAsBlock:
  def __init__(self, text, line_length):
    self.text, self.translator = adjust_line_lengths(text, line_length).values()