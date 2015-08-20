'''
Created on 16 juil. 2012

@author: openerp
'''
import pygtk
pygtk.require('2.0')
import gtk
import random

STANDARD_SIZE = 40

KEY_LEFT = 65361
KEY_UP = 65362
KEY_RIGHT= 65363
KEY_DOWN = 65364

class CaseElement():

    level = 5

    def get_info(self):
        pass

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
        return False

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

    def to_scale(self, length, place=0):
        return  place * self.size + length * self.size / STANDARD_SIZE

    def next_turn(self):
        print "city next turn"
        self.inhabitant = int(self.inhabitant * (1 + 0.05))

    def get_info(self):
        return "%s : %s (%s Citizen)" % (self.player and self.player.name or "Barbarian", self.name, self.inhabitant)


    def get_buttons(self):
        create_unit = gtk.Button("Recruite")
        create_unit.connect("clicked", self.__callback_recruit)
        build =  gtk.Button("Build")
        return ('City', [create_unit, build])



    def __callback_recruit(self, widget):
        print "recruitement", self.player.name

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
        self.pressed = False

    def add_city(self, name):
        city = City(self, name)
        self.case_elements[city.level] = city

    def get_info(self):
        info = ""
        for element in self.case_elements.values():
            info += element.get_info()

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


class Map():



    def __init__(self, parent, size, reso=20, city_nb=0):
        self.parent = parent
        self.city_range = 2
        self.map = {}
        self.reso = reso
        self.size = size
        city_nb = city_nb or self.size[0] * self.size[1] / ( (self.city_range +2)**2 + 5)
        print (self.city_range * 2 +1)**2
        for i in xrange(0, size[0]):
            for j in xrange(0, size[1]):
                self.map[(i,j)] = Case(self, (i, j), self.reso)
        self._init_city(city_nb)
        self.pressed = False

    def _init_city(self, city_nb):
        def check_coordo(coordo):
            area = []
            for i in range(-self.city_range, self.city_range + 1):
                for j in range(-self.city_range, self.city_range + 1):
                    area.append((coordo[0] + i, coordo[1] + j))
            return any([c in done_coordo for c in area])

        if city_nb > self.size[0] * self.size[1] / (self.city_range +2)**2:
            raise Exception("Too much city")
        done_coordo = []
        for i in xrange(0, city_nb):
            coordo = (random.randint(0, self.size[0]-1), random.randint(0, self.size[1] -1))
            while check_coordo(coordo):
                coordo = (random.randint(0, self.size[0] -1), random.randint(0, self.size[1] -1))
            self.map[coordo].add_city("%s - %s" % coordo)
            if i < len(self.parent.players):
                self.map[coordo].set_player(self.parent.players[i])

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
            self.parent.side_panel.reset_command_button()
            for title, buttons in self.map[x,y].get_buttons_frames():
                self.parent.side_panel.display_command_button(title, buttons)
            self.pressed = (x,y)

    def key_pressed(self, widget, event):
        print event.keyval


    def next_turn(self):
        for case in self.map.values():
            case.next_turn()

