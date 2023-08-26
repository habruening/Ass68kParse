import gi

gi.require_version("WebKit2", "4.0")
from gi.repository import WebKit2, Gtk, GLib

def make_editor():
  decoding_box = Gtk.Box()
  x = Gtk.Label(label="", xalign=0)
  x.set_markup('<span background="white"><tt>        </tt></span>')
  x.set_margin_left(8)
  decoding_box.pack_start(x, False, True, 0)
  return decoding_box
