# All this code is very experimental

import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from listingfile import assembly_code_68k

import assembly_viewer.listing_file_viewer as listing_view
import assembly_interpreter.hex_decoder
import assembly_interpreter.assembler_instructions
import assembly_program.assembly_file
import instruction_view.assembly_decoding_help as instruction_bits_view
import instruction_view.assembly_html_help as instruction_manual_view
import instruction_editor.assembly_editor as instruction_editor_view
import user_interface.ui as gui

from gi.repository import Gdk

file_name = "tests/listingfile/TestData/JCOBITCP_JCOBTCC.LIS"
all_lines = assembly_program.assembly_file.open_assembly_file(file_name)
file = open(file_name).read().replace("\f"," ")

gui.start_gui()
file_in_view = listing_view.create_listing_file_viewer(file, all_lines, gui.take_widget_as_left_view)
gui.take_widget_as_left_view(instruction_editor_view.make_editor())
gui.take_widget_as_left_view(instruction_editor_view.make_editor())

help_functions = None

def add_help():
  global help_functions
  instruction_manual = instruction_manual_view.make_view(gui.take_widget_into_right_view("html_help"))
  help_functions = lambda instruction, new_instruction : update_help(instruction_manual, instruction, new_instruction)
  gui.take_widget_into_right_view("instruction_bits")(instruction_bits_view.make_decoding_help())
  
def disable_help():
  global help_functions
  gui.close_right_view()
  help_functions = None

bit_to_highlight = -1

def update_help(instruction_manual, instruction, new_instruction):
  global bit_to_highlight
  gui.close_from_right_view("instruction_bits")
  
  if type(instruction) == assembly_code_68k.Instruction:
    opcode = assembly_interpreter.hex_decoder.make_bits_from_hex_string(str(instruction.opcode))
    instruction = assembly_interpreter.assembler_instructions.decode_instruction(str(instruction.opcode))
    if instruction:
      instruction_manual.show_instruction(instruction, bit_to_highlight, new_instruction)
    gui.take_widget_into_right_view("instruction_bits")(instruction_bits_view.show_instruction(opcode, bit_to_highlight))
  else:
    gui.take_widget_into_right_view("instruction_bits")(instruction_bits_view.show_no_instruction())
    instruction_manual.show_text("")
    bit_to_highlight = -1

  gui.right_container.show_all()

def create_instruction_editor():
  gui.take_widget_as_left_view(instruction_editor_view.make_editor())
  gui.take_widget_as_left_view(instruction_editor_view.make_editor())
  gui.show_all()

def on_key_press_event(window, event):
  global bit_to_highlight
  global help_functions
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
  elif keyname == "F6":
    create_instruction_editor()
  elif keyname == "F8":
    if help_functions:
      disable_help()
    else:
      add_help()
  else:
    return
  file_in_view.mark_current_page()
  file_in_view.mark_current_line()
  file_in_view.place_cursor()
  if help_functions:
    help_functions(file_in_view.current_line(), new_instruction)
  return True

gui.set_key_press_event(on_key_press_event)
gui.run_gui_as_main_loop()