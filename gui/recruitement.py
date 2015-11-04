# coding: utf8
'''
Created on 23 août 2015

@author: odoo
'''
import pygtk
import Player
pygtk.require('2.0')
import gtk

from builder import interface, DialogGlade




class Recruitement(DialogGlade):

    def __init__(self, city):
        self.city  = city
        self.dialog = interface.get_object('recruitement_dialog')
        self.dialog.connect("delete-event", self.close)
        self.dialog.show_all()
        self.scale = interface.get_object('recruitement_scale')
        self.scale.set_adjustment(gtk.Adjustment(value=20, lower=0, upper=100, step_incr=1, page_incr=10, page_size=10))
        self.scale.clear_marks()
        self.scale.add_mark(50, 0, "50")

        interface.get_object("cancel_recruitement").connect("clicked", self.close)
        self.ok_button = interface.get_object("ok_recruitement")
        self.recruit_handler = self.ok_button.connect("clicked", self.recruit)

    def recruit(self, widget):
        self.city.recruit(self.scale.get_value())
        self.dialog.hide()
        self.ok_button.disconnect(self.recruit_handler)
