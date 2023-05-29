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
  
listing_file_viewer = assembly_viewer.listing_file_viewer.ListingFileViewer(file, all_lines)
    


  
html = "<h1>This is HTML content</h1><p>I am displaying this in python</p"



gi.require_version("WebKit2", "4.0")
from gi.repository import WebKit2, Gtk, GLib

view = WebKit2.WebView()
view.load_html(html)

def on_key_press_event(window, event):
  keyname = Gdk.keyval_name(event.keyval)
  if keyname == "Down":
    listing_file_viewer.selection.set_selection_to_line_after()
  if keyname == "Up":
    listing_file_viewer.selection.set_selection_to_line_before()
  listing_file_viewer.selection.select_page()
  listing_file_viewer.selection.select_line()
  listing_file_viewer.place_corsur()
  return True

win.connect("key-press-event",on_key_press_event)

box.pack_start(listing_file_viewer.widget(), True, True, 0)
box.pack_start(view, True, True, 0)


win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()