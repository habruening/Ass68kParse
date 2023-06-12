import gi

gi.require_version("WebKit2", "4.0")
from gi.repository import WebKit2, Gtk, GLib

from threading import Timer

import io

def make_view():
  
  view = WebKit2.WebView()
  settings = view.get_settings()
  settings.set_enable_javascript(True)
  view.set_settings(settings)
  html = "undef"
  view.load_html(html)
  return view

def show_instruction(view, instruction, bit_to_highlight, field_to_highlight, field_value, new_instruction):
  html = open("assembly_manual/html/Sec. 4, {}.html".format(instruction)).read()
  if instruction == "MOVEQ":
    # This is a work around, because AJAX does not work.
    html_regs = ""
    if field_to_highlight == "register":
      html_regs = open("assembly_manual/html/Sec. 1, 1.1.1 Data Registers (D7 – D0).html").read().replace('"', '\\"').replace("\n", "\\n")
    def red():
      java_script_command = 'load_register_manual("'+html_regs+'")'
      view.evaluate_javascript(java_script_command, -1, None, None, None, None, None)

    t = Timer(0.1, red)
    t.start()

  def red():
    field_value_ = "".join(["1" if bit else "0" for bit in field_value])
    java_script_command = 'highlight_bit("{}", {}, "{}")'.format(field_value_, bit_to_highlight, field_to_highlight)
    view.evaluate_javascript(java_script_command, -1, None, None, None, None, None)
  t = Timer(0.1, red)
  t.start()

  if new_instruction:
    view.load_html(html)
  view.show_all()  

def show_text(view, text):
  view.load_html(text)
  view.show_all()    