'''
Created on 16 juil. 2012

@author: openerp
'''
import pygtk
pygtk.require('2.0')
import gtk
import random

STANDARD_SIZE = 40

class CaseElement():
    def get_info(self):
        pass
    
    def next_turn(self):
        pass
    
    def draw(self, drawable, gc):
        pass
    
    def set_player(self, player):
        pass
    
    def get_level(self):
        return 5

class City(CaseElement):
    def __init__(self, parent, name, inhabitant=100):
        self.parent = parent
        self.name = name
        self.inhabitant = inhabitant
        self.player = False
        self.color = "black"
        self.size = self.parent.size
        
    def set_player(self, player):
        self.player = player
        self.color = player.color
    
    def draw(self, drawable, gc):
        (x, y) = self.parent.coordo
        
        gc.set_rgb_fg_color(gtk.gdk.color_parse(self.color))
        size = self.size
        

        drawable.draw_rectangle(gc, False, self.to_scale(5, x), self.to_scale(5, y), size + self.to_scale(-11), size + self.to_scale(-11))
        drawable.draw_rectangle(gc, False, self.to_scale(8, x), self.to_scale(8, y), size + self.to_scale(-17), size + self.to_scale(-17))
        drawable.draw_rectangle(gc, True, self.to_scale(15, x), self.to_scale(10, y), size + self.to_scale(-29), size + self.to_scale(-32))
        drawable.draw_rectangle(gc, True, self.to_scale(10, x), self.to_scale(22, y), size + self.to_scale(-24), size + self.to_scale(-33))
           
    def to_scale(self, length, place=0):
        return  place * self.size + length * self.size / STANDARD_SIZE
        
    def next_turn(self):
        print "city next turn"
        self.inhabitant = int(self.inhabitant * (1 + 0.05))

    def get_info(self):
        return "%s : %s (%s Citizen)" % (self.player and self.player.name or "Barbarian", self.name, self.inhabitant)
    
    def get_level(self):
        return 2
    
class Case():
    
    def __init__(self, parent, coordo, size=20):
        self.parent = parent
        self.coordo = coordo
        self.size = size
        self.pressed = False
        self.case_elements = {} 
        
    def draw(self, drawable, gc):
        if self.pressed:
            gc.set_rgb_fg_color(gtk.gdk.color_parse("blue"))
        else:
            gc.set_rgb_fg_color(gtk.gdk.color_parse("green"))
        drawable.draw_rectangle(gc, False, self.coordo[0] * self.size , self.coordo[1]* self.size, self.size-1, self.size-1)
        
        for element in self.case_elements.values():
            element.draw(drawable, gc)
            
            
            
    def button_pressed(self):
        self.pressed = True
        self.parent.parent.side_panel
    
    def reset(self):
        print 'reset case'
        self.pressed = False
        
    def add_city(self, name):
        city = City(self, name)
        self.case_elements[city.get_level()] = city
        
    def get_info(self):
        info = ""
        for element in self.case_elements.values():
            info += element.get_info()
        
        if not info:
            return "Free"
        else:
            return info
        
    def next_turn(self):
        for element in self.case_elements.values():
            element.next_turn()
            
    def set_player(self, player):
        for element in self.case_elements.values():
            element.set_player(player)
        
        
class Map():
    def __init__(self, parent, size, reso=20, city_nb=12):
        self.parent = parent
        self.map = {}
        self.reso = reso
        self.size = size
        city_nb = city_nb or self.size[0] * self.size[1] / 20
        for i in xrange(0, size[0]):
            for j in xrange(0, size[1]):
                self.map[(i,j)] = Case(self, (i, j), self.reso)
        self._init_city(city_nb)
        self.pressed = False

    def _init_city(self, city_nb):
        def check_coordo(coordo):
            area = []
            for i in [-2,-1,0,1,2]:
                for j in [-2,-1,0,1,2]:
                    area.append((coordo[0] + i, coordo[1] + j))
            return any([c in done_coordo for c in area])
        
        if city_nb > self.size[0] * self.size[1] / 25:
            raise Exception("Too much city")
        done_coordo = []
        for i in xrange(0, city_nb):
            coordo = (random.randint(0, self.size[0]-1), random.randint(0, self.size[1] -1))
            while check_coordo(coordo):
                coordo = (random.randint(0, self.size[0] -1), random.randint(0, self.size[1] -1))
            self.map[coordo].add_city("%s - %s" % coordo)
            done_coordo.append(coordo)
                
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
            #self.map[x,y].set_player(self.parent.player['Player 1'])
            self.parent.side_panel.set_case_info(self.map[x,y].get_info())
            self.pressed = (x,y)
            
    def next_turn(self):
        for case in self.map.values():
            case.next_turn()
        
        