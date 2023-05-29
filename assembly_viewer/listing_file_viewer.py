
import gi
from gi.repository import Gtk, Pango, Gdk
gi.require_version("Gtk", "3.0")


from assembly_viewer import format_as_block
from listingfile import assembly_code_68k


class ListingFileViewer():


  def __init__(self, listing_file):
    self.scrolledwindow = Gtk.ScrolledWindow()
    self.scrolledwindow.set_hexpand(True)
    self.scrolledwindow.set_vexpand(True)

    self.textview = Gtk.TextView()
    self.textview.modify_font(Pango.FontDescription("mono"))
    self.textview.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0.04))

    self.text = format_as_block.TextAsBlock(listing_file, 132)
    self.textview.get_buffer().set_text(self.text.text)


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

  def make_highlighter(self, lines):
    on_display = [tuple(map( lambda from_to : self.text.translator.source_to_target(from_to), content.raw.from_to))
                     for content in lines]
    [tuple(map( lambda from_to : self.text.translator.source_to_target(from_to), content.raw.from_to))
                     for content in lines]

    selections = [tuple(map( lambda from_to : self.pointer_to_position(from_to), selection))
                     for selection in on_display]
    return selections

class ContentSelector:
  def __init__(self, listing_file_viewer, all_lines):
    self.line_number = 0
    self.line_selections = []
    self.page_selection = False
    self.listing_file_viewer = listing_file_viewer
    self.all_lines = all_lines

  def select_line(self):
    for selection in self.line_selections:
      self.listing_file_viewer.remove_tag("line", selection)
      self.listing_file_viewer.remove_tag("ass_line", selection)
      self.listing_file_viewer.remove_tag("branch_line", selection)
    self.line_selections.clear()
    self.line_selections.extend(self.listing_file_viewer.make_highlighter(self.all_lines[self.line_number].lines))
    for selection in self.line_selections:
      self.listing_file_viewer.apply_tag("line", selection)
    if type(self.all_lines[self.line_number]) == assembly_code_68k.Instruction:
      instruction = self.all_lines[self.line_number]
      syntax_selections = self.listing_file_viewer.make_highlighter(instruction.address + instruction.opcode + instruction.mnemonic + instruction.arguments)
      self.line_selections.extend(syntax_selections)
      for selection in syntax_selections:
        self.listing_file_viewer.apply_tag("ass_line", selection)
      branch_selections = self.listing_file_viewer.make_highlighter(list([go_to.name for go_to in instruction.go_to]))
      for selection in branch_selections:
        self.listing_file_viewer.apply_tag("branch_line", selection)
      self.line_selections.extend(branch_selections)
    elif type(self.all_lines[self.line_number]) == assembly_code_68k.Label:
      label = self.all_lines[self.line_number]
      syntax_selections = self.listing_file_viewer.make_highlighter(label.name)
      self.line_selections.extend(syntax_selections)
      for selection in syntax_selections:
        self.listing_file_viewer.apply_tag("ass_line", selection)
      branch_selections = self.listing_file_viewer.make_highlighter(list([come_from.line for come_from in label.come_from]))
      for selection in branch_selections:
        self.listing_file_viewer.apply_tag("branch_line", selection)
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
    selected_text = tuple(map( lambda from_to : self.listing_file_viewer.text.translator.source_to_target(from_to), selected_content))
    self.page_selection = tuple(map( lambda from_to : self.listing_file_viewer.textbuffer().get_iter_at_offset(from_to), selected_text))
    self.listing_file_viewer.apply_tag("page", self.page_selection)
