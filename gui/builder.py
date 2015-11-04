# coding: utf8
'''
Created on 23 août 2015

@author: odoo
'''
import pygtk
pygtk.require('2.0')
import gtk

interface = gtk.Builder()

class DialogGlade():
    def close(self, widget, *args):
        widget.hide()
        return True