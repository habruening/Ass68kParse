# All this code is very experimental

import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from listingfile import listing_file_68k
from listingfile import printed_file
from assembly_viewer import format_as_block
from listingfile import assembly_code_68k

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk

win = Gtk.Window()
win.set_default_size(1100, 700)

scrolledwindow = Gtk.ScrolledWindow()
scrolledwindow.set_hexpand(True)
scrolledwindow.set_vexpand(True)

textview = Gtk.TextView()
textbuffer = textview.get_buffer()
textview.modify_font(Pango.FontDescription("mono"))
textview.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0.04))
ifile = open("tests/listingfile/TestData/JCOBITCP_JCOBTCC.LIS").read().replace("\f"," ")
text = format_as_block.TextAsBlock(ifile, 132)
textbuffer.set_text(text.text)
scrolledwindow.add(textview)

all_lines_orig = listing_file_68k.open_file("tests/listingfile/TestData/JCOBITCP_JCOBTCC.LIS")

all_lines = []
assembler_code = []
for line in all_lines_orig:
  if assembly_code_68k.decode_instruction(line):
    instruction = assembly_code_68k.decode_instruction(line)
    instruction.lines = line.lines
    all_lines.append(instruction)
    assembler_code.append(instruction)
    instruction.go_to = []
  elif assembly_code_68k.decode_label(line):
    label = assembly_code_68k.decode_label(line)
    label.lines = line.lines
    all_lines.append(label)
    assembler_code.append(label)
    label.come_from = []
  else:
    all_lines.append(line)

for label in (l for l in assembler_code if type(l) == assembly_code_68k.Label):
  for instruction in (i for i in assembler_code if type(i) == assembly_code_68k.Instruction):
    if(str(label.name) == str(instruction.arguments)):
      instruction.go_to.append(label)
      label.come_from.append(instruction)
  

def make_highlighter(lines):
    on_display = [tuple(map( lambda from_to : text.translator.source_to_target(from_to), content.raw.from_to))
                     for content in lines]
    selections = [tuple(map( lambda from_to : textbuffer.get_iter_at_offset(from_to), selection))
                     for selection in on_display]
    return selections

class ContentSelector:
  def __init__(self):
    self.line_number = 0
    self.line_selections = []
    self.page_selection = False
    self.tags = {"line" : textbuffer.create_tag("yellow_bg", background="yellow"),
                 "ass_line" : textbuffer.create_tag("orange_bg", background="orange") ,
                 "branch_line" : textbuffer.create_tag("green_bg", foreground="red", background="white") ,
                 "page" : textbuffer.create_tag("white_bg", background="white") }

  def apply_tag(self, tag, selection):
    for i in self.tags.values():
      textbuffer.remove_tag(i, selection[0], selection[1])
    textbuffer.apply_tag(self.tags[tag], selection[0], selection[1])

  def select_line(self):
    for selection in self.line_selections:
      textbuffer.remove_tag(self.tags["line"], selection[0], selection[1])
      textbuffer.remove_tag(self.tags["ass_line"], selection[0], selection[1])
      textbuffer.remove_tag(self.tags["branch_line"], selection[0], selection[1])
    self.line_selections.clear()
    self.line_selections.extend(make_highlighter(all_lines[self.line_number].lines))
    for selection in self.line_selections:
      self.apply_tag("line", selection)
    if type(all_lines[self.line_number]) == assembly_code_68k.Instruction:
      instruction = all_lines[self.line_number]
      syntax_selections = make_highlighter(instruction.address + instruction.opcode + instruction.mnemonic + instruction.arguments)
      self.line_selections.extend(syntax_selections)
      for selection in syntax_selections:
        self.apply_tag("ass_line", selection)
      branch_selections = make_highlighter(list([go_to.name for go_to in instruction.go_to]))
      for selection in branch_selections:
        self.apply_tag("branch_line", selection)
      self.line_selections.extend(branch_selections)
    elif type(all_lines[self.line_number]) == assembly_code_68k.Label:
      label = all_lines[self.line_number]
      syntax_selections = make_highlighter(label.name)
      self.line_selections.extend(syntax_selections)
      for selection in syntax_selections:
        self.apply_tag("ass_line", selection)
      branch_selections = make_highlighter(list([come_from.line for come_from in label.come_from]))
      for selection in branch_selections:
        self.apply_tag("branch_line", selection)
      self.line_selections.extend(branch_selections)

  def select_page(self):
    if self.page_selection:
      textbuffer.remove_tag(self.tags["page"], self.page_selection[0], self.page_selection[1])
    selected_line = all_lines[self.line_number]
    selected_page = selected_line.lines[0].page_header + selected_line.lines[0].page_content
    selected_content = (selected_page[0].from_to[0], selected_page[-1].from_to[1])
    selected_text = tuple(map( lambda from_to : text.translator.source_to_target(from_to), selected_content))
    self.page_selection = tuple(map( lambda from_to : textbuffer.get_iter_at_offset(from_to), selected_text))
    self.apply_tag("page", self.page_selection)

selection = ContentSelector()
    
def on_key_press_event(window, event):
  global selection
  keyname = Gdk.keyval_name(event.keyval)
  if keyname == "Down":
    while (selection.line_number < len(all_lines) - 1):
      selection.line_number = selection.line_number + 1
      if str(all_lines[selection.line_number]):
        break
  if keyname == "Up":
    while 0 < selection.line_number:
      selection.line_number = selection.line_number - 1
      if str(all_lines[selection.line_number]):
        break
  selection.select_page()
  selection.select_line()
  textbuffer.place_cursor(selection.line_selections[0][0])
  return True

def on_cursor_changed(a, b):
  cursor_position = text.translator.target_to_source(textbuffer.props.cursor_position)
  def find_subline():
    selected_line = 0
    while(True):
      for sl in all_lines[selected_line].lines:
        if cursor_position < sl.raw.from_to[1]:
          return selected_line
      selected_line = selected_line + 1
  selection.line_number = find_subline()
  selection.select_page()
  selection.select_line()
  
win.connect("key-press-event",on_key_press_event)
textbuffer.connect("notify::cursor-position",on_cursor_changed)

win.add(scrolledwindow)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()