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
  return view

def show_instruction(view, instruction, bit_to_highlight, field_to_highlight, field_value, new_instruction):
  def after_load():
    field_value_ = "".join(["1" if bit else "0" for bit in field_value])
    java_script_command = 'highlight_bit("{}", "{}", {}, "{}")'.format(instruction.lower(), field_value_, bit_to_highlight, field_to_highlight)
    view.evaluate_javascript(java_script_command, -1, None, None, None, None, None)
  t = Timer(0.1, after_load)
  t.start()

  if new_instruction:
    view.load_uri("file:/home/hartmut/Ass68kParse/assembly_manual/html/Sec. 4, {}.html".format(instruction))
  view.show_all()  

def show_text(view, text):
  view.load_html(text)
  view.show_all()    