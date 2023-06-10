import gi

gi.require_version("WebKit2", "4.0")
from gi.repository import WebKit2, Gtk, GLib

from threading import Timer

def make_view():
  
  view = WebKit2.WebView()
  settings = view.get_settings()
  settings.set_enable_javascript(True)
  view.set_settings(settings)
  html = "undef"
  view.load_html(html)
  return view

def show_instruction(view, instruction, bit_to_highlight, field_to_highlight, new_instruction):
  html = "undef"
  if instruction == "MOVEQ":
    html_regs = ""
    html = open("assembly_manual/html/Sec. 4, MOVEQ.html").read()
    if 4 <= bit_to_highlight and bit_to_highlight <= 6:
      html_regs = open("assembly_manual/html/Sec. 1, 1.1.1 Data Registers (D7 – D0).html").read().replace('"', '\\"').replace("\n", "\\n")
    def red():
      java_script_command = 'highlight_bit({}, "{}")'.format(bit_to_highlight, field_to_highlight)
      view.evaluate_javascript(java_script_command, -1, None, None, None, None, None)
      java_script_command = 'load_register_manual("'+html_regs+'")'
      view.evaluate_javascript(java_script_command, -1, None, None, None, None, None)

    t = Timer(0.1, red)
    t.start()

  if instruction == "MOVE":
    html = open("assembly_manual/html/Sec. 4, MOVE.html").read()
    def red():
      java_script_command = 'highlight_bit({}, "{}")'.format(bit_to_highlight, field_to_highlight)
      view.evaluate_javascript(java_script_command, -1, None, None, None, None, None)

    t = Timer(0.1, red)
    t.start()
  if new_instruction:
    view.load_html(html)
  view.show_all()  

def show_text(view, text):
  view.load_html(text)
  view.show_all()    