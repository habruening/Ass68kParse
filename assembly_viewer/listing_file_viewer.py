
import gi
from gi.repository import Gtk, Pango, Gdk
gi.require_version("Gtk", "3.0")


from assembly_viewer import format_as_block
from listingfile import assembly_code_68k

#def create_listing_viewer(listing_file, all_lines, give_away_widget):
  

class ListingFileViewer():

  def __init__(self, listing_file, all_lines, give_widget_away):

    self.text = format_as_block.TextAsBlock(listing_file, 132)
  
    scrolledwindow = Gtk.ScrolledWindow()
    give_widget_away(scrolledwindow)
    textview = Gtk.TextView()
    textview.modify_font(Pango.FontDescription("mono"))
    textview.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0.04))
    self.text_buffer = textview.get_buffer()
    self.text_buffer.set_text(self.text.text)
    scrolledwindow.add(textview)

    self.tags = {"line" : self.text_buffer.create_tag("yellow_bg", background="yellow"),
                 "ass_line" : self.text_buffer.create_tag("orange_bg", background="orange") ,
                 "branch_line" : self.text_buffer.create_tag("green_bg", foreground="red", background="white") ,
                 "page" : self.text_buffer.create_tag("white_bg", background="white") }
    
    self.selection = ContentSelector(self, all_lines)

    def cursor_moved():
      cursor_position = self.text.translator.target_to_source(self.text_buffer.props.cursor_position)
      def find_subline():
        selected_line = 0
        while(True):
          for sl in all_lines[selected_line].lines:
            if cursor_position < sl.raw.from_to[1]:
              return selected_line
          selected_line = selected_line + 1
      self.selection.line_number = find_subline()
      self.selection.select_page()
      self.selection.select_line()

    self.text_buffer.connect("notify::cursor-position",lambda a , b : cursor_moved())


  def get_selection(self, lines):
    on_screen = [(self.text.translator.source_to_target(snip[0]),
                   self.text.translator.source_to_target(snip[1])) for snip in lines]
    return [(self.text_buffer.get_iter_at_offset(snip[0]),
             self.text_buffer.get_iter_at_offset(snip[1])) for snip in on_screen]
             
  def apply_tag(self, tag, selection):
    # To be used only with things that are created by get_selection
    for snip in selection:
      for i in self.tags.values():
        self.text_buffer.remove_tag(i, snip[0], snip[1])
      self.text_buffer.apply_tag(self.tags[tag], snip[0], snip[1])

  def remove_tag(self, tag, selection):
    # To be used only with things that are created by get_selection
    for snip in selection:
      self.text_buffer.remove_tag(self.tags[tag], snip[0], snip[1])

def raw_of(text_elements):
  return [(snip.raw.from_to[0], snip.raw.from_to[1]) for snip in text_elements]

class ContentSelector:
  def __init__(self, listing_file_viewer, all_lines):
    self.line_number = 0
    self.line_selections = []
    self.page_selection = False
    self.listing_file_viewer = listing_file_viewer
    self.all_lines = all_lines

  def selected_line(self):
    return self.all_lines[self.line_number]

  def select_line(self):
    self.listing_file_viewer.remove_tag("line", self.line_selections)
    self.listing_file_viewer.remove_tag("ass_line", self.line_selections)
    self.listing_file_viewer.remove_tag("branch_line", self.line_selections)
    self.line_selections.clear()
    self.line_selections.extend(self.listing_file_viewer.get_selection(raw_of(self.all_lines[self.line_number].lines)))
    self.listing_file_viewer.apply_tag("line", self.line_selections)
    if type(self.all_lines[self.line_number]) == assembly_code_68k.Instruction:
      instruction = self.all_lines[self.line_number]
      syntax_selections = self.listing_file_viewer.get_selection(raw_of(instruction.address + instruction.opcode + instruction.mnemonic + instruction.arguments))
      self.line_selections.extend(syntax_selections)
      self.listing_file_viewer.apply_tag("ass_line", syntax_selections)
      branch_selections = self.listing_file_viewer.get_selection(raw_of(list([go_to.name for go_to in instruction.go_to])))
      self.listing_file_viewer.apply_tag("branch_line", branch_selections)
      self.line_selections.extend(branch_selections)
    elif type(self.all_lines[self.line_number]) == assembly_code_68k.Label:
      label = self.all_lines[self.line_number]
      syntax_selections = self.listing_file_viewer.get_selection(raw_of(label.name))
      self.line_selections.extend(syntax_selections)
      self.listing_file_viewer.apply_tag("ass_line", syntax_selections)
      branch_selections = self.listing_file_viewer.get_selection(raw_of(list([come_from.line for come_from in label.come_from])))
      self.listing_file_viewer.apply_tag("branch_line", branch_selections)
      self.line_selections.extend(branch_selections)

  def set_selection_to_line_before(self):
    while 0 < self.line_number:
      self.line_number = self.line_number - 1
      if str(self.all_lines[self.line_number]):
        break

  def set_selection_to_line_after(self):
    while (self.line_number < len(self.all_lines) - 1):
      self.line_number = self.line_number + 1
      if str(self.all_lines[self.line_number]):
        break

  def select_page(self):
    if self.page_selection:
      self.listing_file_viewer.remove_tag("page", self.page_selection)
    selected_line = self.all_lines[self.line_number]
    selected_page = selected_line.lines[0].page_header + selected_line.lines[0].page_content
    selected_content = (selected_page[0].from_to[0], selected_page[-1].from_to[1])
    self.page_selection = self.listing_file_viewer.get_selection([selected_content])
    self.listing_file_viewer.apply_tag("page", self.page_selection)

  def place_corsur(self):
    self.listing_file_viewer.text_buffer.place_cursor(self.line_selections[0][0])
