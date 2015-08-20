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
        self.player_turn = gtk.Label(self.game.get_current_player().name + ' Turn')
        self.label_property = gtk.Label("Property :")
        self.label_case_info = gtk.Label("Info Case : ")
        self.button_next_turn = gtk.Button("End Turn")
        self.button_next_turn.set_can_focus(False)
        self.button_next_turn.connect("clicked", self.next_turn)

        self.button_vbox = gtk.VBox(False, 0)



        self.pack_start(self.player_turn)
        self.pack_start(self.label_property)
        self.pack_start(self.label_case_info)
        self.pack_start(self.button_vbox)
        self.pack_start(self.button_next_turn)



    def set_coordo(self, x, y):
        self.label_property.set_text("Coordo : (%s, %s)" % (x, y))

    def set_case_info(self, message):
        self.label_case_info.set_text(message)

    def next_turn(self, widget, data=None):
        self.game.next_turn()


    def refresh_turn(self):
        self.player_turn.set_text(self.game.get_current_player().name + ' Turn')


    def reset_command_button(self):
        for widget in self.button_vbox.get_children():
            self.button_vbox.remove(widget)
        self.game.window.show_all()

    def display_command_button(self, title, buttons):
        print "display command button"
        frame = gtk.Frame(title)
        bbox = gtk.HButtonBox()

        bbox.set_border_width(5)
        bbox.set_layout(gtk.BUTTONBOX_START)
        bbox.set_spacing(10)
        for button in buttons:
            button.set_can_focus(False)
            bbox.add(button)

        frame.add(bbox)
        self.button_vbox.pack_start(frame)
        self.game.window.show_all()

