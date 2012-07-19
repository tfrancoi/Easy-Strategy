'''
Created on 16 juil. 2012

@author: openerp
'''
import pygtk
pygtk.require('2.0')
import gtk

class CaseElement():
    def get_info(self):
        pass
    
    def next_turn(self):
        pass
    
    def draw(self, drawable, gc):
        pass

class City(CaseElement):
    def __init__(self, parent, name, inhabitant=100):
        self.parent = parent
        self.name = name
        self.inhabitant = inhabitant
    
    def draw(self, drawable, gc):
        (x, y) = self.parent.coordo
        size = self.parent.size
        gc.set_rgb_fg_color(gtk.gdk.color_parse("black"))
        drawable.draw_rectangle(gc, False, x * size + 5, y * size + 5, size- 11, size-11)
        drawable.draw_rectangle(gc, False, x * size + 8, y * size + 8, size- 17, size-17)
        drawable.draw_rectangle(gc, True, x * size + 15, y * size + 10, size- 29, size-32)
        drawable.draw_rectangle(gc, True, x * size + 10, y * size + 22, size- 24, size-33)
        
    def next_turn(self):
        print "city next turn"
        self.inhabitant = int(self.inhabitant * (1 + 0.05))

    def get_info(self):
        return "%s (%s Citizen)" % (self.name, self.inhabitant)
    
class Case():
    
    def __init__(self, parent, coordo, size=20):
        self.parent = parent
        self.coordo = coordo
        self.size = size
        self.pressed = False
        self.city = None
        self.case_elements = {} 
        
    def draw(self, drawable, gc):
        if self.pressed:
            gc.set_rgb_fg_color(gtk.gdk.color_parse("blue"))
        else:
            gc.set_rgb_fg_color(gtk.gdk.color_parse("green"))
        drawable.draw_rectangle(gc, False, self.coordo[0] * self.size , self.coordo[1]* self.size, self.size-1, self.size-1)
        
        if self.city:
            self.city.draw(drawable, gc)
            
            
            
    def button_pressed(self):
        self.pressed = True
        self.parent.parent.side_panel
    
    def reset(self):
        self.pressed = False
        
    def add_city(self, name):
        self.city = City(self, name)
        
    def get_info(self):
        if self.city:
            return "City : " + self.city.get_info()
        else:
            return "Free"
        
    def next_turn(self):
        if self.city:
            self.city.next_turn()
        
class Map():
    def __init__(self, parent, size, reso=20):
        self.parent = parent
        self.map = {}
        self.reso = reso
        for i in xrange(0, size[0]):
            for j in xrange(0, size[1]):
                self.map[(i,j)] = Case(self, (i, j), self.reso)
                if i ==  j*j  or 20 - j == i * 2:
                    self.map[(i,j)].add_city("%s - %s" % (i, j))
        self.pressed = False
                
    def draw(self, drawable, gc):
        for case in self.map.values():
            case.draw(drawable, gc)
        
    def button_pressed(self, pixel_x, pixel_y):
        if self.pressed:
            self.map[self.pressed].reset()
        x = int(pixel_x / self.reso)
        y = int(pixel_y / self.reso)
        if self.map.get((x, y)):
            self.parent.side_panel.set_coordo(x, y)
            self.map[x,y].button_pressed()
            self.parent.side_panel.set_case_info(self.map[x,y].get_info())
            self.pressed = (x,y)
            
    def next_turn(self):
        for case in self.map.values():
            case.next_turn()
        
        