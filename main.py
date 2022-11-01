# Solitaire game, based on https://api.arcade.academy/en/latest/tutorials/card_game/index.html

import arcade
import random

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

# The Y of the top row (4 piles)
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row (7 piles)
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# Espaciado al que están las pilas
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT
# Espaciado que tiene cada carta cuando está una encima de otra
CARD_VERTICAL_OFFSET = CARD_HEIGHT * CARD_SCALE * 0.3

CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]  # Declaramos las cartas
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# Constantes para representar cada pila individualmente
PILE_COUNT = 13
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1
PLAY_PILE_1 = 2
PLAY_PILE_2 = 3
PLAY_PILE_3 = 4
PLAY_PILE_4 = 5
PLAY_PILE_5 = 6
PLAY_PILE_6 = 7
PLAY_PILE_7 = 8
TOP_PILE_1 = 9
TOP_PILE_2 = 10
TOP_PILE_3 = 11
TOP_PILE_4 = 12


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

        arcade.set_background_color(arcade.color.AMAZON)  # Hacemos la ventana de color verde

        self.card_list = None  # Creamos una lista donde van a ir metidas todas las cartas, el llamado "mazo"

        self.held_cards = None  # Declaramos las cartas que tomamos con el mouse

        self.held_cards_original_position = None  # Posicion original de las cartas cuando las movemos

        self.pile_mat_list = None  # Esta pila la vamos a duplicar para crear las 8 pilas del juego

        self.piles = None  # Esto es una lista que tiene listas de cartas dentro, podemos verla como la "mesa"

    def setup(self):  # Esta funcion nos sirve para reiniciar el juego

        self.held_cards = []
        # Aca ya inicializamos la posicion original de las cartas
        self.held_cards_original_position = []

        self.setup_piles()  # Hacemos el llamado a la funcion de crear las pilase sto son los sprite donde van metidas

        self.card_list = arcade.SpriteList()

        for card_sign in CARD_SUITS:
            for card_value in CARD_VALUES:
                card_aux = card(card_sign, card_value, CARD_SCALE)
                card_aux.position = START_X, BOTTOM_Y  # Esto es para llenar nuestra lista con cada una de las cartas
                self.card_list.append(card_aux)  # nuestras cartas son los "sprite"

        self.shuffle_cards()

        # Inicializamos la lista de listas que va a tener 13 espacios, nuestra "mesa"
        self.piles = [[] for _ in range(PILE_COUNT)]

        # Metemos nuestro mazo a esta nueva lista de listas
        for card_aux in self.card_list:
            self.piles[BOTTOM_FACE_DOWN_PILE].append(card_aux)

    def setup_piles(self):

        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()  # Creamos la lista de sprites o "pilas"

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, BOTTOM_Y  # Esto le agrega el fondo verde a nuestro mazo de cartas
        self.pile_mat_list.append(pile)

        # Aca estamos creando un sprite a la par del mazo para cuando damos vuelta a una carta
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Creamos las 7 pilas de juego
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Ademas creamos 4 mas donde van los A
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

    def on_draw(self):
        # Renderiza los sprite
        self.clear()
        self.pile_mat_list.draw()
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
        # Busca la pila más cercana
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        # Comprueba si tocamos alguna pila
        if arcade.check_for_collision(self.held_cards[0], pile):

            # Que pila es?
            pile_index = self.pile_mat_list.index(pile)

            #  Si estamos en la misma pila simplemente la devuelve a su posicion original
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                pass

            # Si estamos en las 7 pilas de juego podemos hacer lo siguiente:
            elif PLAY_PILE_1 <= pile_index <= PLAY_PILE_7:

                # Comprueba si hay cartas en esa pila
                if len(self.piles[pile_index]) > 0:
                    # Mueve las cartas
                    top_card = self.piles[pile_index][-1]
                    for i, dropped_card in enumerate(self.held_cards):
                        dropped_card.position = top_card.center_x, \
                                                top_card.center_y - CARD_VERTICAL_OFFSET * (i + 1)
                else:

                    # Si no hay cartas en esa posicion
                    for i, dropped_card in enumerate(self.held_cards):
                        # Mueve las cartas
                        dropped_card.position = pile.center_x, \
                                                pile.center_y - CARD_VERTICAL_OFFSET * i

                for card_aux in self.held_cards:
                    # Movemos la carta a la pila correcta
                    self.move_card_to_new_pile(card_aux, pile_index)

                # No resetee su posicion
                reset_position = False

            # En caso de que queramos mover cartas a las pilas de arriba
            elif TOP_PILE_1 <= pile_index <= TOP_PILE_4 and len(self.held_cards) == 1:

                self.held_cards[0].position = pile.position
                # Mueve la carta a la lista
                for card_aux in self.held_cards:
                    self.move_card_to_new_pile(card_aux, pile_index)

                reset_position = False

        if reset_position:

            for pile_index, card_aux in enumerate(self.held_cards):
                card_aux.position = self.held_cards_original_position[pile_index]

        # No estamos tomando ninguna carta
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):

        # Si estamos tomando una carta la podemos mover de un lado a otro
        for card_aux in self.held_cards:
            card_aux.center_x += dx
            card_aux.center_y += dy

    def pull_to_top(self, card_aux: arcade.Sprite):

        # Quita la carta de un lado y la borra
        self.card_list.remove(card_aux)
        self.card_list.append(card_aux)

    def shuffle_cards(self):
        # Metodo general para revolver las cartas
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

    def get_pile_for_card(self, card_aux):
        # Le mandamos una carta y nos devuelve en la pila que se encuentra
        for index, pile in enumerate(self.piles):
            if card_aux in pile:
                return index

    def remove_card_from_pile(self, card_aux):
        # Le damos una carta y la quita de la pila en que se encuentra
        for pile in self.piles:
            if card_aux in pile:
                pile.remove(card_aux)
                break

    def move_card_to_new_pile(self, card_aux, pile_index):
        # Le damos una carta, una pila y la mueve a esa pila específicamente
        self.remove_card_from_pile(card_aux)
        self.piles[pile_index].append(card_aux)


def main():
    window = solitaire()  # Declaramos nuestro main y hacemos los respectivos llamados
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
