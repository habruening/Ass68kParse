import gi

gi.require_version("WebKit2", "4.0")
from gi.repository import WebKit2, Gtk, GLib

from threading import Timer

def make_view():  
  view = WebKit2.WebView()
  settings = view.get_settings()
  settings.set_enable_javascript(True)
  settings.set_allow_file_access_from_file_urls(True)
  view.set_settings(settings)
  view.load_html("")
  class EmptyClass:
    pass
  to_return = EmptyClass()
  to_return.show_instruction = lambda instruction, bit_to_highlight, new_instruction : show_instruction(view, instruction, bit_to_highlight, new_instruction)
  to_return.show_text = lambda text : show_text(view, text)
  to_return.view = view
  return to_return

def js_call(instruction, args):
  return instruction + "(" + ",".join(args) + ")"

def js_string(text):
  return "'"+text+"'"

def show_instruction(view, instruction, bit_to_highlight, new_instruction):
  field_name = instruction.get_field_of_bit(bit_to_highlight)
  js_fields = {field : str(instruction.fields[field].bin) for field in instruction.fields}
  js_command = \
"{                                                            \n" +\
  "let instr_name = '{}';                                     \n".format(instruction.name.lower()) +\
  "let instr_fields = {}                                      \n".format(str(js_fields)) +\
  "let bit_no = {};                                           \n".format(bit_to_highlight) +\
  "let field_name = '{}';                                     \n".format(field_name) +\
  "highlight_bit(instr_name,instr_fields,bit_no,field_name);\n" +\
"}"
  js_command = js_call("highlight_bit",
  #  instruction_name,                    bit_no,               instruction_fields, field_name
    [js_string(instruction.name.lower()), str(bit_to_highlight), str(js_fields),     js_string(field_name)])
  print(js_command)
  def after_load():
    view.evaluate_javascript(js_command, -1, None, None, None, None, None)
  t = Timer(0.1, after_load)
  t.start()

  if new_instruction:
    view.load_uri("file:/home/hartmut/Ass68kParse/instruction_manual/html/Sec. 4, {}.html".format(instruction.name))
  view.show_all()  

def show_text(view, text):
  view.load_html(text)
  view.show_all()    