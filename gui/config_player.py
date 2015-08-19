import pygtk
import Player
pygtk.require('2.0')
import gtk



class ConfigPlayer():

    def __init__(self, interface, game):
        self.game = game
        self.interface = interface
        self.dialog = interface.get_object('config_player')
        self.dialog.show_all()

        for i in xrange(1,5):
            color_chooser_button = self.interface.get_object("player%s_color_chooser_button" % i)
            color_chooser_button.connect("clicked", self.choose_color, i)

        new_game = self.interface.get_object("button_new_game")
        new_game.connect("clicked", self.new_game_clicked)

    def choose_color(self, widget, player):
        color_chooser = gtk.ColorSelectionDialog("Pick a color")
        response = color_chooser.run()
        if response == gtk.RESPONSE_OK:
            couleur = color_chooser.colorsel.get_current_color().to_string()
            color_text = self.interface.get_object("player%s_color" % player)
            color_text.set_text(couleur)

        color_chooser.hide()

    def new_game_clicked(self, widget):
        self._get_player(1)
        all_player = []
        for i in range(1,5):
            player = self._get_player(i)
            if player:
                all_player.append(player)
        self.dialog.hide()
        self.game.new_game(all_player)

    def _get_player(self, player_nb):
        name = self.interface.get_object("player%s_name" % player_nb).get_text()
        color = self.interface.get_object("player%s_color" % player_nb).get_text()
        player_type = self.interface.get_object("player%s_type" % player_nb).get_active_text()
        if player_type != Player.NOT_PLAYING:
            return Player.Player(name, color, player_type)
        return False