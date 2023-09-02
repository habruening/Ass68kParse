import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk

gtk_window = 0
layout = 0

right_container = 0
right_widgets = []
left_view_widgets = []

def show_all():
  right_container.show_all();
  for widget in left_view_widgets:
    widget.show_all()

def start_gui():
  global gtk_window
  global layout
  gtk_window = Gtk.Window()
  gtk_window.set_default_size(1300, 800)
  layout = Gtk.Box(spacing=6)
  layout.set_homogeneous(True)
  gtk_window.add(layout)

  
def take_widget_as_left_view(widget):
  global layout
  global left_view_widgets
  left_view_widgets.append(widget)
  layout.pack_start(widget, True, True, 0)
  widget.set_hexpand(True)
  widget.set_vexpand(True)

def take_widget_into_right_view(widget):
  global right_container
  global layout
  if not(right_container):
    right_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    layout.pack_start(right_container, True, True, 0)
    right_container.pack_start(widget, True, True, 0)
  else:
    right_container.pack_start(widget, False, True, 10)
  right_widgets.append(widget)
  right_container.show_all()

def close_right_view():
  global right_container
  global right_widgets
  if right_container:
    right_container.destroy()
    right_container = 0
    right_widgets = []
  
def close_last_from_right_view():
  global right_widgets
  right_widgets[-1].destroy()
  right_widgets = right_widgets[:-1]

def set_key_press_event(key_press_event):
  gtk_window.connect("key-press-event",key_press_event)
  
def run_gui_as_main_loop():
  global gtk_window
  gtk_window.connect("destroy", Gtk.main_quit)
  gtk_window.show_all()
  Gtk.main()