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

all_lines = listing_file_68k.open_file("tests/listingfile/TestData/JCOBITCP_JCOBTCC.LIS")

class ContentSelector:
  def __init__(self):
    self.line_number = 0
    self.line_selections = []
    self.page_selection = False
    self.tags = {"line" : textbuffer.create_tag("yellow_bg", background="yellow"),
                 "ass_line" : textbuffer.create_tag("orange_bg", background="orange") ,
                 "page" : textbuffer.create_tag("white_bg", background="white") }

  def apply_tag(self, tag, selection):
    for i in self.tags.values():
      textbuffer.remove_tag(i, selection[0], selection[1])
    textbuffer.apply_tag(self.tags[tag], selection[0], selection[1])

  def select_line(self):
    for selection in self.line_selections:
      textbuffer.remove_tag(self.tags["line"], selection[0], selection[1])
      textbuffer.remove_tag(self.tags["ass_line"], selection[0], selection[1])
    selected_line = all_lines[self.line_number]
    selected_content = selected_line.lines
    selected_text = [tuple(map( lambda from_to : text.translator.source_to_target(from_to), content.raw.from_to))
                     for content in selected_content]
    self.line_selections = [tuple(map( lambda from_to : textbuffer.get_iter_at_offset(from_to), selection))
                     for selection in selected_text]
    line_type = "line"
    if assembly_code_68k.decode_instruction(str(all_lines[self.line_number])):
      line_type = "ass_line"
    elif assembly_code_68k.decode_label(str(all_lines[self.line_number])):
      line_type = "ass_line"
    for selection in self.line_selections:
      self.apply_tag(line_type, selection)

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