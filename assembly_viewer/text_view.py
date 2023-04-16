# All this code is very experimental

import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from listingfile import listing_file_68k
from assembly_viewer import format_as_block

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

tag = textbuffer.create_tag("orange_bg", background="orange")
ptag = textbuffer.create_tag("white_bg", background="white")
selection = []
pselection = False

all_lines = listing_file_68k.open_file("tests/listingfile/TestData/JCOBITCP_JCOBTCC.LIS")
selected_line = 0

def select_line():
  global selected_line
  global selection
  global pselection
  if pselection:
    textbuffer.remove_tag(ptag, pselection[0], pselection[1])
  pselection = (all_lines[selected_line][0].page_header[0].from_to[0], all_lines[selected_line][0].page_content[-1].from_to[1])
  pselection = (text.translator.source_to_target(pselection[0]), text.translator.source_to_target(pselection[1]))
  pselection = (textbuffer.get_iter_at_offset(pselection[0]), textbuffer.get_iter_at_offset(pselection[1]))
  textbuffer.apply_tag(ptag, pselection[0], pselection[1])
  for sl in selection:
    textbuffer.remove_tag(tag, sl[0], sl[1])
  def subline_to_selection(sl):
    return (textbuffer.get_iter_at_offset(text.translator.source_to_target(sl.content.from_to[0])), textbuffer.get_iter_at_offset(text.translator.source_to_target(sl.content.from_to[1])))
  selection = [(subline_to_selection(sl)) for sl in all_lines[selected_line]]
  for sl in selection:
    textbuffer.remove_tag(ptag, sl[0], sl[1])
    textbuffer.apply_tag(tag, sl[0], sl[1])    

def on_key_press_event(window, event):
  global selected_line
  global selection
  keyname = Gdk.keyval_name(event.keyval)
  if keyname == "Down":
    while (selected_line < len(all_lines) - 1):
      selected_line = selected_line + 1
      if all_lines[selected_line][0].content.from_to[1] - all_lines[selected_line][0].content.from_to[0]:
        break
  if keyname == "Up":
    while 0 < selected_line:
      selected_line = selected_line - 1
      if all_lines[selected_line][0].content.from_to[1] - all_lines[selected_line][0].content.from_to[0]:
        break
  select_line()
  textbuffer.place_cursor(selection[0][0])
  return True

def on_cursor_changed(a, b):
  global selected_line
  cursor_position = text.translator.target_to_source(textbuffer.props.cursor_position)
  def find_subline():
    selected_line = 0
    while(True):
      for sl in all_lines[selected_line]:
        if cursor_position < sl.content.from_to[1]:
          return selected_line
      selected_line = selected_line + 1
  selected_line = find_subline()
  select_line()

win.connect("key-press-event",on_key_press_event)
textbuffer.connect("notify::cursor-position",on_cursor_changed)

win.add(scrolledwindow)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()