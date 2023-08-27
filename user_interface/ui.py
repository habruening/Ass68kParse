import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk

gtk_window = 0
layout = 0

def start_gui():
  global gtk_window
  global layout
  gtk_window = Gtk.Window()
  gtk_window.set_default_size(1300, 800)
  layout = Gtk.Box(spacing=6)
  gtk_window.add(layout)
  
def take_main_widget(widget):
  layout.pack_start(widget, True, True, 0)
  layout.set_homogeneous(True)
  widget.set_hexpand(True)
  widget.set_vexpand(True)
