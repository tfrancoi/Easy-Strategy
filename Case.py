# coding: utf8
'''
Created on 16 juil. 2012

@author: openerp
'''
import pygtk
from gui import recruitement
pygtk.require('2.0')
import gtk

STANDARD_SIZE = 40



class CaseElement():

    level = 5

    def get_info(self):
        return ''

    def next_turn(self):
        pass

    def draw(self, drawable, gc):
        pass

    def set_player(self, player):
        pass

    def get_buttons(self):
        """
            return (title, buttons)
                where title will be the title of the frame and buttons the list of buttons specific to this case
        """
        return ('', [])

    def to_scale(self, length, place=0):
        return  place * self.size + length * self.size / STANDARD_SIZE


class Unit(CaseElement):

    level = 5

    def __init__(self, parent, qty, player):
        self.parent = parent
        self.qty = qty
        self.player = player
        self.color = self.player.color
        self.size = self.parent.size

    def draw(self, drawable, gc):
        (x, y) = self.parent.coordo

        gc.set_rgb_fg_color(gtk.gdk.color_parse(self.color))
        size = self.size
        #TODO
        drawable.draw_arc(gc, True, self.to_scale(12, x), self.to_scale(12, y), size + self.to_scale(-24), size + self.to_scale(-24), 0,360 * 64)
        drawable.draw_arc(gc, False, self.to_scale(10, x), self.to_scale(10, y), size + self.to_scale(-20), size + self.to_scale(-20), 0,360 * 64)

    def get_info(self):
        return 'Unit Player %s, size %s' % (self.player.name, self.qty)

class City(CaseElement):

    level = 2

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


    def next_turn(self):
        self.inhabitant = int(self.inhabitant * (1 + 0.05))

    def get_info(self):
        return "%s : %s (%s Citizen)" % (self.player and self.player.name or "Barbarian", self.name, self.inhabitant)


    def get_buttons(self):
        if self.player == self.parent.parent.parent.get_current_player():
            create_unit = gtk.Button("Recruite")
            create_unit.connect("clicked", self.__callback_recruit)
            build =  gtk.Button("Build")
            return ('City', [create_unit, build])
        else:
            return ('', [])



    def __callback_recruit(self, widget):
        if self.player:
            recruitement.Recruitement(self)

    def recruit(self, qty):
        self.inhabitant -= qty
        print self.player
        unit = Unit(self.parent, qty, self.player)
        self.parent.add_unit(unit)
        self.parent.parent.case_pressed(self.parent)

class Case():

    def __init__(self, parent, coordo, size=20):
        self.parent = parent
        self.coordo = coordo
        self.size = size
        self.pressed = False
        self.case_elements = {}

    def draw(self, drawable, gc):
        if self.pressed:
            gc.set_rgb_fg_color(gtk.gdk.color_parse("red"))
        else:
            gc.set_rgb_fg_color(gtk.gdk.color_parse("green"))
        drawable.draw_rectangle(gc, False, self.coordo[0] * self.size , self.coordo[1]* self.size, self.size-1, self.size-1)

        for element in self.case_elements.values():
            element.draw(drawable, gc)


    def button_pressed(self):
        self.pressed = True
        self.parent.parent.side_panel

    def reset(self):
        self.pressed = False

    def add_city(self, name):
        city = City(self, name)
        self.case_elements[city.level] = city

    def add_unit(self, unit):
        self.case_elements[unit.level] = unit

    def get_info(self):
        info = ""
        for element in self.case_elements.values():
            info += element.get_info() + "\n"

        if not info:
            return "Free"
        else:
            return info

    def get_buttons_frames(self):
        info = []
        for element in self.case_elements.values():
            info.append(element.get_buttons())
        return info

    def next_turn(self):
        for element in self.case_elements.values():
            element.next_turn()

    def set_player(self, player):
        for element in self.case_elements.values():
            element.set_player(player)


