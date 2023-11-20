# Some workarounds for Python limitations

class EmptyClass:
  pass

def set(dict, key):
  def set(value):
    dict[key] = value
  return set

# Rectangle as Class

class Rectangle:
  def __init__(self, x, y):
      self.x = x
      self.y = y
  def set_x(self, x):
    self.x = x
  def circumference(self):
     return 2*self.x + 2*self.y 
  
my_rect = Rectangle(10, 20);
print(my_rect.circumference())
my_rect.set_x(20)
print(my_rect.circumference())

# Rectangle with data Dict

def createRectangle(x,y):
  self = {"x" : x, "y" : y}
  result = EmptyClass()
  result.set_x = set(self, "x")
  result.circumference = lambda : circumference([self["x"]], [self["y"]])
  return result

def circumference(x, y):
  return 2*x[0] + 2*y[0]

my_rect = createRectangle(10, 20);
print(my_rect.circumference())
my_rect.set_x(20)
print(my_rect.circumference())

# Rectangle as pure dict

def createRectangle(x,y):
  self = {"x" : x, "y" : y}
  return {"set_x" : set(self, "x"),
          "circumference" : lambda : circumference([self["x"]], [self["y"]])}

def circumference(x, y):
  return 2*x[0] + 2*y[0]

# Rectangle as pure dict better readable

x, y, set_x, circumference = range(4)

def createRectangle(x,y):
  self = {x : x, y : y}
  return {set_x : set(self, x),
          circumference : lambda : circumference([self[x]], [self[y]])}

def circumference(x, y):
  return 2*x[0] + 2*y[0]

# In functional languages

def createRectangle(x,y):
  return {"x" : x, "y" : y}

def set_x(rectangle, value):
  rectangle["x"] = value

def circumference(rectangle):
  return 2*rectangle["x"] + 2*rectangle["y"]

my_rect = createRectangle(10, 20);
print(circumference(my_rect))
set_x(my_rect, 20)
print(circumference(my_rect))
