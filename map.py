# coding: utf8
'''
Created on 23 août 2015

@author: odoo
'''
from Case import Case
import random

KEY_LEFT = 65361
KEY_UP = 65362
KEY_RIGHT= 65363
KEY_DOWN = 65364

def translation(coordo, trans):
    return coordo[0] + trans[0], coordo[1] + trans[1]

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

        x = int(pixel_x / self.reso)
        y = int(pixel_y / self.reso)
        if self.map.get((x, y)):
            self._case_pressed(x, y)

    def case_pressed(self, case):
        return self._case_pressed(case.coordo[0], case.coordo[1])

    def _case_pressed(self, x, y):
        if self.pressed:
            self.map[self.pressed].reset()
        self.parent.side_panel.set_coordo(x, y)
        self.map[x,y].button_pressed()
        #self.map[x,y].set_player(self.parent.player['Player 1'])
        self.parent.side_panel.set_case_info(self.map[x,y].get_info())
        self.parent.side_panel.reset_command_button()
        for title, buttons in self.map[x,y].get_buttons_frames():
            self.parent.side_panel.display_command_button(title, buttons)
        self.pressed = (x,y)

    def key_pressed(self, event):
        #print event.keyval
        key_translation = {
            KEY_DOWN : (0,1),
            KEY_UP : (0, -1),
            KEY_LEFT: (-1, 0),
            KEY_RIGHT: (1, 0),
        }
        if self.pressed and key_translation.get(event.keyval):
            x, y = translation(self.pressed, key_translation[event.keyval])
            if self._coordo_in_map((x, y)):
                self.map[self.map[self.pressed].move_to((x,y))]
                self._case_pressed(x, y)

    def _coordo_in_map(self, coordo):
        x = coordo[0]
        y = coordo[1]
        return x >= 0 and x < self.size[0] and y >= 0 and y < self.size[1]

    def next_turn(self):
        for case in self.map.values():
            case.next_turn()

    def get_case(self, coordo):
        if self._coordo_in_map(coordo):
            return self.map[coordo]
        return False
