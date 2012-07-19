'''
Created on 17 juil. 2012

@author: openerp
'''

import pygtk
pygtk.require('2.0')
import gtk

class SidePanel(gtk.VBox):
    def __init__(self, game):
        super(SidePanel, self).__init__()
        self.game = game
        label = gtk.Label("Hello")
        self.label_property = gtk.Label("Property :")
        self.label_case_info = gtk.Label("Info Case : ")
        self.button_next_turn = gtk.Button("End Turn")
        self.button_next_turn.connect("clicked", self.next_turn)
        
        self.pack_start(label)
        self.pack_start(self.label_property)
        self.pack_start(self.label_case_info)
        self.pack_start(self.button_next_turn)
    
    def set_coordo(self, x, y):
        self.label_property.set_text("Coordo : (%s, %s)" % (x, y))
    
    def set_case_info(self, message):
        self.label_case_info.set_text(message)
        
    def next_turn(self, widget, data=None):
        self.game.map.next_turn()
        
if __name__ == "__main__":
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.add(SidePanel())
    window.show()
    gtk.main()