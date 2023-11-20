import gi

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk
from gi.repository import WebKit2, Gtk, GLib

from threading import Timer


win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)
view = WebKit2.WebView()

html = """<!DOCTYPE html>
<html>
<body>
<p id="demo">This is an AJAX test.</p>
<button type="button" onclick='document.getElementById("demo").innerHTML = "Ajax works."'>Change Content</button>
</body>
</html>
"""
view.load_html(html)
settings = view.get_settings()
settings.set_enable_javascript(True)
win.add(view)


def hello():
  view.evaluate_javascript('document.getElementById("demo").innerHTML = "Ajax works."', -1, None, None, None, None, None)
  print("done")

t = Timer(2.0, hello)
t.start() # after 30 seconds, "hello, world" will be printed


win.show_all()
Gtk.main()