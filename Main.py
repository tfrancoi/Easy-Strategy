#!/usr/bin/env python
# example drawingarea.py

import pygtk
from Case import Case, Map
from SidePanel import SidePanel
pygtk.require('2.0')
import gtk




    


class DrawingAreaExample:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Drawing Area Example")
        window.connect("destroy", gtk.main_quit)
        self.side_panel = SidePanel(self)
        self.map = Map(self, (20,10), 40)
        self.hbox = gtk.HBox()
        self.area = gtk.DrawingArea()
        self.area.set_size_request(800, 400)
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
        window.add(self.hbox)
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
    

if __name__ == "__main__":
    DrawingAreaExample()
    gtk.main()