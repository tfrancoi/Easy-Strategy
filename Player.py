'''
Created on 20 juil. 2012

@author: openerp
'''
PLAYER = "Player"
IA = "IA"
NOT_PLAYING = "Not Playing"
class Player():

    def __init__(self, name, color, type="Player"):
        self.name = name
        self.color = color