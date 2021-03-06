#!/usr/bin/env python
# example drawingarea.py

import pygtk
from Case import Unit
pygtk.require('2.0')
import gtk

from gui.SidePanel import SidePanel
from gui import config_player
from gui.builder import interface

from Player import Player
from map import Map

class Game:
    def __init__(self):
        interface.add_from_file('gui.glade')
        interface.connect_signals(self)
        self.players = []

        self.window = interface.get_object('window1')
        self.window.set_title("Easy strategy")
        self.window.connect("destroy", gtk.main_quit)

        self.side_panel = SidePanel(self)
        hbox = interface.get_object('hbox1')
        hbox.pack2(self.side_panel)

        self.window.set_default_size(800, 500)
        self.window.show_all()

    def expose_handler(self, widget, event):
        xgc = widget.window.new_gc()
        if self.map:
            self.map.draw(widget.window, xgc)

    def button_press_event(self, widget, event):
        if self.map:
            self.map.button_pressed(event.x, event.y)
        widget.queue_draw()
        widget.grab_focus()

    def key_pressed_event(self, widget, event):
        if self.map:
            self.map.key_pressed(event)
        widget.queue_draw()

    def push_new(self, widget):
        config_player.ConfigPlayer(self)

    def new_game(self, players):
        self.players = players
        self.current_player = 0
        case_size=40
        map_size=(20,15)
        self.map = Map(self, map_size, case_size)
        self.side_panel.refresh_turn()
        self.area = gtk.DrawingArea()
        self.area.set_flags(gtk.CAN_FOCUS)
        self.area.set_size_request(map_size[0] * case_size, map_size[1] * case_size)
        self.area.connect("expose-event", self.expose_handler)
        self.area.connect("button_press_event", self.button_press_event)
        self.area.connect("key_press_event", self.key_pressed_event)
        self.area.set_events(gtk.gdk.EXPOSURE_MASK
                             | gtk.gdk.LEAVE_NOTIFY_MASK
                             | gtk.gdk.BUTTON_PRESS_MASK
                             | gtk.gdk.POINTER_MOTION_MASK
                             | gtk.gdk.POINTER_MOTION_HINT_MASK
                             | gtk.gdk.KEY_PRESS_MASK)

        scroll_panel = interface.get_object('scrolledwindow1')
        scroll_panel.add_with_viewport(self.area)

        self.window.queue_draw()
        self.window.show_all()

    def get_current_player(self):
        if not self.players:
            return Player('', 'black')
        return self.players[self.current_player]

    def next_turn(self):
        self.map.next_turn() # if current player = 0 then next turn of the case
        self.current_player = (self.current_player + 1) % len(self.players)
        self.side_panel.refresh_turn()


if __name__ == "__main__":
    g = Game()
    p1 = Player("Player 1", "red")
    g.new_game([p1, Player("Player 2", "blue")])
    g.map.map[(1,1)].add_unit(Unit(g.map.map[(1,1)], 10, p1))
    gtk.main()
