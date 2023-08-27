# All this code is very experimental

import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from listingfile import assembly_code_68k

import assembly_viewer.listing_file_viewer
import assembly_interpreter.hex_decoder
import assembly_interpreter.assembler_instructions
import assembly_program.assembly_file

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk

import user_interface.ui

file_name = "tests/listingfile/TestData/JCOBITCP_JCOBTCC.LIS"
all_lines = assembly_program.assembly_file.open_assembly_file(file_name)
file = open(file_name).read().replace("\f"," ")

    
import instruction_view.assembly_decoding_help
import instruction_view.assembly_html_help


user_interface.ui.start_gui()
file_in_view = assembly_viewer.listing_file_viewer.create_listing_file_viewer(file, all_lines, user_interface.ui.take_main_widget)

help_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

view = instruction_view.assembly_html_help.make_view()
help_box.pack_end(view.view, True, True, 0)

decoding_box = instruction_view.assembly_decoding_help.make_decoding_help()
help_box.pack_start(decoding_box, False, True, 10)

user_interface.ui.layout.pack_start(help_box, True, True, 0)
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
    file_in_view.set_selection_to_line_after()
  elif keyname == "Up":
    file_in_view.set_selection_to_line_before()
  elif keyname == "Left":
    bit_to_highlight -= 1
    new_instruction = False
  elif keyname == "Right":
    bit_to_highlight += 1
    new_instruction = False
  else:
    return
  file_in_view.select_page()
  file_in_view.select_line()
  file_in_view.place_corsur()
  update_html(file_in_view.current_line(), new_instruction)
  return True

user_interface.ui.gtk_window.connect("key-press-event",on_key_press_event)
user_interface.ui.gtk_window.connect("destroy", Gtk.main_quit)
user_interface.ui.gtk_window.show_all()
Gtk.main()