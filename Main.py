#!/usr/bin/env python
# example drawingarea.py

import pygtk
from Case import Case, Map
from SidePanel import SidePanel
pygtk.require('2.0')
import gtk
from Player import Player




    


class DrawingAreaExample:
    menu_bar = False
    
    def __init__(self, case_size=40, map_size=(20,15)):
        self.player = {}
        self.player['Player 1'] = Player('Player 1', 'blue')
        self.player['Player 2'] = Player('Player 2', 'yellow')
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Drawing Area Example")
        window.connect("destroy", gtk.main_quit)
        self.side_panel = SidePanel(self)
        self.map = Map(self, map_size, case_size)
        self.hbox = gtk.HBox()
        self.area = gtk.DrawingArea()
        self.area.set_size_request(map_size[0] * case_size, map_size[1] * case_size)
        self.area.connect("expose-event", self.expose_handler)
        self.area.connect("button_press_event", self.button_press_event)
        self.area.set_events(gtk.gdk.EXPOSURE_MASK 
                             | gtk.gdk.LEAVE_NOTIFY_MASK 
                             | gtk.gdk.BUTTON_PRESS_MASK 
                             | gtk.gdk.POINTER_MOTION_MASK
                             | gtk.gdk.POINTER_MOTION_HINT_MASK)
        #self.area.show()
        #self.side_panel.show()
        self.hbox.pack_start(self.area)
        self.hbox.pack_start(self.side_panel)
        #self.hbox.show()
        vbox = gtk.VBox(False, 2)
        vbox.pack_start(self.get_menu_bar())
        vbox.pack_start(self.hbox)
        window.add(vbox)
        window.show_all()
        
    def expose_handler(self, widget, event):
        xgc = widget.window.new_gc()
        xgc.set_rgb_fg_color(gtk.gdk.color_parse("yellow"))
        self.map.draw(widget.window, xgc)
        
    def button_press_event(self, widget, event):
        print event.x, event.y
        #self.side_panel.set_coordo(event.x, event.y)
        self.map.button_pressed(event.x, event.y)
        widget.queue_draw()
    
    def get_menu_bar(self):
        if not self.menu_bar:
            self.menu_bar = gtk.MenuBar()
    
            filemenu = gtk.Menu()
            filem = gtk.MenuItem("File")
            filem.set_submenu(filemenu)
           
            exit_button = gtk.MenuItem("Exit")
            exit_button.connect("activate", gtk.main_quit)
            filemenu.append(exit_button)
    
            self.menu_bar.append(filem)
        return self.menu_bar

if __name__ == "__main__":
    DrawingAreaExample()
    gtk.main()