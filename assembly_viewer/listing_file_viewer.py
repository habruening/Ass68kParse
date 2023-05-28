
import gi
from gi.repository import Gtk, Pango, Gdk
gi.require_version("Gtk", "3.0")

class ListingFileViewer():
  def __init__(self):
    self.scrolledwindow = Gtk.ScrolledWindow()
    self.scrolledwindow.set_hexpand(True)
    self.scrolledwindow.set_vexpand(True)

    self.textview = Gtk.TextView()
    self.textview.modify_font(Pango.FontDescription("mono"))
    self.textview.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0.04))

    self.scrolledwindow.add(self.textview)

  def textbuffer(self):
    return self.textview.get_buffer()
  
  def pointer_to_position(self, position):
    return self.textbuffer().get_iter_at_offset(position)

  def widget(self):
    return self.scrolledwindow