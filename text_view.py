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
import assembly_interpreter.hex_decoder

import assembly_interpreter.assembler_instructions

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
    

import instruction_view.assembly_html_help
import instruction_view.assembly_decoding_help
view = instruction_view.assembly_html_help.make_view()


box.pack_start(listing_file_viewer.widget(), True, True, 0)
box.set_homogeneous(True)
help_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
help_box.pack_end(view.view, True, True, 0)

decoding_box = instruction_view.assembly_decoding_help.make_decoding_help()
help_box.pack_start(decoding_box, False, True, 10)

box.pack_start(help_box, True, True, 0)
bit_to_highlight = -1

def update_html(instruction, new_instruction):
  global decoding_box
  global bit_to_highlight
  decoding_box.destroy()

  if type(instruction) == assembly_code_68k.Instruction:
    opcode = assembly_interpreter.hex_decoder.make_bits_from_hex_string(str(instruction.opcode))
    instruction = assembly_interpreter.assembler_instructions.decode_instruction(str(instruction.opcode))
    if instruction:
      view.show_instruction(instruction, bit_to_highlight, new_instruction)
    decoding_box = instruction_view.assembly_decoding_help.show_instruction(opcode, bit_to_highlight)
  else:
    decoding_box = instruction_view.assembly_decoding_help.show_no_instruction()
    view.show_text("")
    bit_to_highlight = -1

  help_box.pack_start(decoding_box, False, True, 10)
  help_box.show_all()

def on_key_press_event(window, event):
  global bit_to_highlight
  keyname = Gdk.keyval_name(event.keyval)
  new_instruction = True
  if keyname == "Down":
    listing_file_viewer.selection.set_selection_to_line_after()
  elif keyname == "Up":
    listing_file_viewer.selection.set_selection_to_line_before()
  elif keyname == "Left":
    bit_to_highlight -= 1
    new_instruction = False
  elif keyname == "Right":
    bit_to_highlight += 1
    new_instruction = False
  else:
    return
  listing_file_viewer.selection.select_page()
  listing_file_viewer.selection.select_line()
  listing_file_viewer.place_corsur()
  update_html(listing_file_viewer.selection.selected_line(), new_instruction)
  return True

win.connect("key-press-event",on_key_press_event)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()