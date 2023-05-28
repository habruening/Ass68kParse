
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

    self.tags = {"line" : self.textview.get_buffer().create_tag("yellow_bg", background="yellow"),
                 "ass_line" : self.textview.get_buffer().create_tag("orange_bg", background="orange") ,
                 "branch_line" : self.textview.get_buffer().create_tag("green_bg", foreground="red", background="white") ,
                 "page" : self.textview.get_buffer().create_tag("white_bg", background="white") }

  def textbuffer(self):
    return self.textview.get_buffer()
  
  def pointer_to_position(self, position):
    return self.textbuffer().get_iter_at_offset(position)

  def widget(self):
    return self.scrolledwindow
  
  def apply_tag(self, tag, selection):
    for i in self.tags.values():
      self.textbuffer().remove_tag(i, selection[0], selection[1])
    self.textbuffer().apply_tag(self.tags[tag], selection[0], selection[1])

  def remove_tag(self, tag, selection):
    self.textbuffer().remove_tag(self.tags[tag], selection[0], selection[1])
