
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk


from assembly_viewer import format_as_block
from listingfile import assembly_code_68k
  
def create_listing_file_viewer(listing_file, all_lines, give_widget_away):

  listing_file_viewer = ListingFileViewer(listing_file, give_widget_away)

  file = AssemblyFileInView(listing_file_viewer, all_lines)

  listing_file_viewer.text_buffer.connect("notify::cursor-position",
        lambda a , b : file.set_line_number_to_position(listing_file_viewer.get_cursor_position()))

  return file

class ListingFileViewer():

  def __init__(self, listing_file, give_widget_away):

    text = format_as_block.TextAsBlock(listing_file, 132)
    self.translator = text.translator
  
    scrolledwindow = Gtk.ScrolledWindow()
    give_widget_away(scrolledwindow)
    textview = Gtk.TextView()
    textview.modify_font(Pango.FontDescription("mono"))
    textview.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0.04))
    self.text_buffer = textview.get_buffer()
    self.text_buffer.set_text(text.text)
    scrolledwindow.add(textview)

    self.markings = {"line" : self.text_buffer.create_tag("yellow_bg", background="yellow"),
                     "ass_line" : self.text_buffer.create_tag("orange_bg", background="orange") ,
                     "branch_line" : self.text_buffer.create_tag("green_bg", foreground="red", background="white") ,
                     "page" : self.text_buffer.create_tag("white_bg", background="white") }

  def get_cursor_position(self):
    return self.translator.target_to_source(self.text_buffer.props.cursor_position)

  def get_selection(self, lines):
    on_screen = [(self.translator.source_to_target(snip[0]),
                   self.translator.source_to_target(snip[1])) for snip in lines]
    return [(self.text_buffer.get_iter_at_offset(snip[0]),
             self.text_buffer.get_iter_at_offset(snip[1])) for snip in on_screen]
             
  def place_cursor_at_begin_of(self, selection):
    self.text_buffer.place_cursor(selection[0][0])

  def mark(self, marking, selection):
    # To be used only with things that are created by get_selection
    for snip in selection:
      for i in self.markings.values():
        self.text_buffer.remove_tag(i, snip[0], snip[1])
      self.text_buffer.apply_tag(self.markings[marking], snip[0], snip[1])

  def unmark(self, marking, selection):
    # To be used only with things that are created by get_selection
    for snip in selection:
      self.text_buffer.remove_tag(self.markings[marking], snip[0], snip[1])

def raw_of(text_elements):
  return [(snip.raw.from_to[0], snip.raw.from_to[1]) for snip in text_elements]

class AssemblyFileInView:
  def __init__(self, listing_file_viewer, all_lines):
    self.line_number = 0
    self.line_selections = []
    self.page_selection = False
    self.listing_file_viewer = listing_file_viewer
    self.all_lines = all_lines

  def current_line(self):
    return self.all_lines[self.line_number]
  
  def mark_line(self, part, marking):
    selection = self.listing_file_viewer.get_selection(part)
    self.line_selections.extend(selection)
    self.listing_file_viewer.mark(marking, selection)
      
  def mark_current_line(self):
    self.listing_file_viewer.unmark("line", self.line_selections)
    self.listing_file_viewer.unmark("ass_line", self.line_selections)
    self.listing_file_viewer.unmark("branch_line", self.line_selections)
    self.line_selections.clear()
    self.mark_line(raw_of(self.all_lines[self.line_number].lines), "line")
    if type(self.all_lines[self.line_number]) == assembly_code_68k.Instruction:
      instruction = self.all_lines[self.line_number]
      self.mark_line(raw_of(instruction.address + instruction.opcode + instruction.mnemonic + instruction.arguments), "ass_line")
      self.mark_line(raw_of([go_to.name for go_to in instruction.go_to]), "branch_line")
    elif type(self.all_lines[self.line_number]) == assembly_code_68k.Label:
      label = self.all_lines[self.line_number]
      self.mark_line(raw_of(label.name), "ass_line")
      self.mark_line(raw_of([come_from.line for come_from in label.come_from]), "branch_line")

  def set_current_line_up(self):
    while 0 < self.line_number:
      self.line_number = self.line_number - 1
      if str(self.all_lines[self.line_number]):
        break

  def set_current_line_down(self):
    while (self.line_number < len(self.all_lines) - 1):
      self.line_number = self.line_number + 1
      if str(self.all_lines[self.line_number]):
        break

  def mark_current_page(self):
    if self.page_selection:
      self.listing_file_viewer.unmark("page", self.page_selection)
    selected_line = self.all_lines[self.line_number]
    selected_page = selected_line.lines[0].page_header + selected_line.lines[0].page_content
    selected_page_content = (selected_page[0].from_to[0], selected_page[-1].from_to[1])
    self.page_selection = self.listing_file_viewer.get_selection([selected_page_content])
    self.listing_file_viewer.mark("page", self.page_selection)

  def place_cursor(self):
    self.listing_file_viewer.place_cursor_at_begin_of(self.line_selections)

  def set_line_number_to_position(self, position):
    def find_subline():
      selected_line = 0
      while(True):
        for sl in self.all_lines[selected_line].lines:
          if position < sl.raw.from_to[1]:
            return selected_line
        selected_line = selected_line + 1
    self.line_number = find_subline()
    self.mark_current_page()
    self.mark_current_line()
