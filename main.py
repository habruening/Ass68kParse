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
file_in_view = assembly_viewer.listing_file_viewer.create_listing_file_viewer(file, all_lines, user_interface.ui.take_widget_as_left_view)

view = 0

def add_help():
  global view
  view = instruction_view.assembly_html_help.make_view(user_interface.ui.take_widget_into_right_view)
  user_interface.ui.take_widget_into_right_view(instruction_view.assembly_decoding_help.make_decoding_help())
 
help_enabled = False

bit_to_highlight = -1

def update_html(instruction, new_instruction):
  global bit_to_highlight
  user_interface.ui.close_last_from_right_view()
  
  if type(instruction) == assembly_code_68k.Instruction:
    opcode = assembly_interpreter.hex_decoder.make_bits_from_hex_string(str(instruction.opcode))
    instruction = assembly_interpreter.assembler_instructions.decode_instruction(str(instruction.opcode))
    if instruction:
      view.show_instruction(instruction, bit_to_highlight, new_instruction)
    user_interface.ui.take_widget_into_right_view(instruction_view.assembly_decoding_help.show_instruction(opcode, bit_to_highlight))
  else:
    user_interface.ui.take_widget_into_right_view(instruction_view.assembly_decoding_help.show_no_instruction())
    view.show_text("")
    bit_to_highlight = -1

  user_interface.ui.right_container.show_all()

def on_key_press_event(window, event):
  global bit_to_highlight
  global help_enabled
  keyname = Gdk.keyval_name(event.keyval)
  new_instruction = True
  if keyname == "Down":
    file_in_view.set_current_line_down()
  elif keyname == "Up":
    file_in_view.set_current_line_up()
  elif keyname == "Left":
    bit_to_highlight -= 1
    new_instruction = False
  elif keyname == "Right":
    bit_to_highlight += 1
    new_instruction = False
  elif keyname == "F8":
    if help_enabled:
      user_interface.ui.close_right_view()
    else:
      add_help()
    help_enabled = not(help_enabled)
  else:
    return
  file_in_view.mark_current_page()
  file_in_view.mark_current_line()
  file_in_view.place_cursor()
  if help_enabled:
    update_html(file_in_view.current_line(), new_instruction)
  return True

user_interface.ui.gtk_window.connect("key-press-event",on_key_press_event)
user_interface.ui.gtk_window.connect("destroy", Gtk.main_quit)
user_interface.ui.gtk_window.show_all()
Gtk.main()