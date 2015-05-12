# Reversi Game

from scene import *
from functools import partial
import sound

class Game (Scene):
    def setup(self):
        self.root_layer = Layer(self.bounds)
        for effect in ['Click_1', 'Click_2', 'Coin_2', 'Coin_5']:
            sound.load_effect(effect)

        self.deal()

    def draw(self):
        background(0.0, 0.2, 0.3)
        self.root_layer.update(self.dt)
        self.root_layer.draw()

    def deal(self):
        images = ['Rabbit_Face', 'Mouse_Face', 'Cat_Face']
        for image in images:
            load_image(image)
#        self.root_layer.sublayers = []
        self.cards = []
        card_size = 48 if self.size.w > 700 else 32
        width = (card_size + 2) * 8
        offset = Point((self.size.w - width)/2,
                       (self.size.h - width)/2)
        for i in xrange(0, 64):
            x, y = i % 8, i / 8
            card = Layer(Rect(offset.x + x * (card_size + 2),
                              offset.y + y * (card_size + 2),
                              card_size, card_size))
            card.card_image = images[0]
            card.background = Color(0.9, 0.9, 0.9)
            card.stroke = Color(1, 1, 1)
            card.stroke_weight = 4.0
            card.index_x = x
            card.index_y = y
            self.add_layer(card)
            self.cards.append(card)
        self.touch_disabled = False

    def touch_began(self, touch):
        if self.touch_disabled:
            return
        for card in self.cards:
            if touch.location in card.frame:
                def reveal_card():
                    card.image = card.card_image
                    card.animate('scale_x', 1.0, 0.15,
                                 completion=None)
#                self.touch_disabled = True
                card.animate('scale_x', 0.0, 0.15,
                             completion=reveal_card)
                card.scale_y = 1.0
                card.animate('scale_y', 0.9, 0.15, autoreverse=True)
                sound.play_effect('Click_1')
                break

    def new_game(self):
        sound.play_effect('Coin_2')
        self.deal()
        self.root_layer.animate('scale_x', 1.0)
        self.root_layer.animate('scale_y', 1.0)

    def win(self):
        self.delay(0.5, partial(sound.play_effect, 'Powerup_2'))
        font_size = 100 if self.size.w > 700 else 50
        text_layer = TextLayer('Well Done!', 'Futura', font_size)
        text_layer.frame.center(self.bounds.center())
        overlay = Layer(self.bounds)
        overlay.background = Color(0, 0, 0, 0)
        overlay.add_layer(text_layer)
        self.add_layer(overlay)
        overlay.animate('background', Color(0.0, 0.2, 0.3, 0.7))
        text_layer.animate('scale_x', 1.3, 0.3, autoreverse=True)
        text_layer.animate('scale_y', 1.3, 0.3, autoreverse=True)
#        self.touch_disabled = True
        self.root_layer.animate('scale_x', 0.0, delay=2.0,
                                curve=curve_ease_back_in)
        self.root_layer.animate('scale_y', 0.0, delay=2.0,
                                curve=curve_ease_back_in,
                                completion=self.new_game)
run(Game())
