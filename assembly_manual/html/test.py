import time
import os

com = input("Command: ")

def open_file(file):
  os.system(file)
 
def delete_file(filefordelete):
  if not(os.path.exists(filefordelete)):
     return print("File does not exist!")
  suretodelete = input("Are you sure? Y/N ")
  if suretodelete == "N" or suretodelete == "n":
     return print("Deleting stopped!")
  if suretodelete != "Y" and suretodelete != "y":
     return
  os.remove(filefordelete)
  print("Deleting successful")

def create_file(filename):
  filename2 = str(filename) + ".txt"
  textinput = input("Text: ")
  with open(filename2, "w") as a:
    a.write(textinput)

commands = {
  "open file"   : lambda : open_file(input("File name: ")),
  "openfile"    : lambda : open_file(input("File name: ")),
  "delete file" : lambda : delete_file(input("File name: ")),
  "deletefile"  : lambda : delete_file(input("File name: ")),
  "create file" : lambda : create_file(input("Name of the file you want to create: ")),
  "createfile"  : lambda : create_file(input("Name of the file you want to create: "))
}

if not(com in commands.keys()):
  print("This command does not exist")

commands[com]()