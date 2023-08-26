import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk

def make_decoding_help():
  decoding_box = Gtk.Box()
  x = Gtk.Label(label="", xalign=0)
  x.set_markup('<span background="white"><tt>        </tt></span>')
  x.set_margin_left(8)
  decoding_box.pack_start(x, False, True, 0)
  return decoding_box

def show_instruction(opcode, highlight_bit):
  decoding_box = Gtk.Box()
  bits = []
  for i in range(len(opcode)):
    x = Gtk.Label(label="", xalign=0)
    bits.append(x)
    if highlight_bit == i:
      x.set_markup('<span background="orange"><tt>'+("1" if opcode[i] else "0")+'</tt></span>')
    else:
      x.set_markup('<span background="white"><tt>'+("1" if opcode[i] else "0")+'</tt></span>')
    if not(i%8):
      x.set_margin_left(8)
    decoding_box.pack_start(x, False, True, 0)
  return decoding_box

def show_no_instruction():
  decoding_box = Gtk.Box()
  x = Gtk.Label(label="", xalign=0)
  x.set_markup('<span background="white"><tt>        </tt></span>')
  x.set_margin_left(8)
  decoding_box.pack_start(x, False, True, 0)
  return decoding_box