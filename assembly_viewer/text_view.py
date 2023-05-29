# All this code is very experimental

import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from listingfile import listing_file_68k
from listingfile import printed_file
from listingfile import assembly_code_68k

import assembly_viewer.listing_file_viewer

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk

win = Gtk.Window()
win.set_default_size(1100, 700)

box = Gtk.Box(spacing=6)
win.add(box)

file = open("tests/listingfile/TestData/JCOBITCP_JCOBTCC.LIS").read().replace("\f"," ")

listing_file_viewer = assembly_viewer.listing_file_viewer.ListingFileViewer(file)

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
  
selection = assembly_viewer.listing_file_viewer.ContentSelector(listing_file_viewer, all_lines)
    
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
  listing_file_viewer.textbuffer().place_cursor(selection.line_selections[0][0])
  return True

def on_cursor_changed(a, b):
  cursor_position = listing_file_viewer.text.translator.target_to_source(listing_file_viewer.textbuffer().props.cursor_position)
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
listing_file_viewer.textbuffer().connect("notify::cursor-position",on_cursor_changed)

box.pack_start(listing_file_viewer.widget(), True, True, 0)

html = "<h1>This is HTML content</h1><p>I am displaying this in python</p"

gi.require_version("WebKit2", "4.0")
from gi.repository import WebKit2, Gtk, GLib

view = WebKit2.WebView()
view.load_html(html)
box.pack_start(view, True, True, 0)


win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()