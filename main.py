# Solitaire game, based on https://api.arcade.academy/en/latest/tutorials/card_game/index.html

import arcade

# Aca declaramos todas las constantes

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Solitaire"

CARD_SCALE = 0.6
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE  # Tamanno de las cartas

MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)  # Tamanno de la mesa donde repartimos las cartas
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

VERTICAL_MARGIN_PERCENT = 0.10  # Estos son los margenes
HORIZONTAL_MARGIN_PERCENT = 0.10

BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]  # Declaramos las cartas
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]


class card(arcade.Sprite):

    def __init__(self, sign, value, scale=1):
        self.sign = sign

        self.value = value

        # Aca se utiliza un png de carta para cuando está volteada
        self.image_file_name = f":resources:images/cards/card{self.sign}{self.value}.png"
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")  # Esto inicializa el tamaño de la carta


class solitaire(arcade.Window):

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)  # Declaramos el tamanno de la ventana

        self.card_list = None  # Creamos una lista donde van a ir metidas todas las cartas, el llamado "mazo"

        arcade.set_background_color(arcade.color.AMAZON)  # Hacemos la ventana de color verde

        # Declaramos las cartas que tomamos con el mouse
        self.held_cards = None

        self.held_cards_original_position = None  # Posicion original de las cartas cuando las movemos

    def setup(self):  # Esta funcion nos sirve para reiniciar el juego

        self.held_cards = []
        # Aca ya inicializamos la posicion original de las cartas
        self.held_cards_original_position = []

        self.card_list = arcade.SpriteList()

        for card_sign in CARD_SUITS:
            for card_value in CARD_VALUES:
                card_aux = card(card_sign, card_value, CARD_SCALE)
                card_aux.position = START_X, BOTTOM_Y  # Esto es para llenar nuestra lista con cada una de las cartas
                self.card_list.append(card_aux)  # nuestras cartas son los "sprite"

    def on_draw(self):
        # Renderiza las cartas
        self.clear()

        self.card_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        # Nos devuelve la lista de cartas en la que dimos click
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Si dimos click el comprueba lo siguiente:
        if len(cards) > 0:
            primary_card = cards[-1]
            # Los demás casos solo toma la que está para arriba
            self.held_cards = [primary_card]
            # Guarda la posicion
            self.held_cards_original_position = [self.held_cards[0].position]
            # La pone encima
            self.pull_to_top(self.held_cards[0])

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):

        if len(self.held_cards) == 0:
            return

        # Si ya no estamos tomando ninguna carta
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):

        # Si estamos tomando una carta la podemos mover de un lado a otro
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def pull_to_top(self, card: arcade.Sprite):

        # Quita la carta de un lado y la borra
        self.card_list.remove(card)
        self.card_list.append(card)


def main():
    window = solitaire()  # Declaramos nuestro main y hacemos los respectivos llamados
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
