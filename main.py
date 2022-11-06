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

# Esta es la imagen que utilizamos para representar las cartas boca abajo
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"

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
        self.is_face_up = False
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def face_down(self):
        # Esto le da vuelta a la carta boca abajo, o más específicamente al "sprite"
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        # Esto pone la carta boca arriba
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        # Esto es un get para ver como es el estado de la carta
        return not self.is_face_up


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

        self.deal_cards()
        self.flip_up_top_cards()

    def setup_piles(self):

        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()  # Creamos la lista de sprites o "pilas"

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, BOTTOM_Y  # Esto le agrega el fondo verde a nuestro mazo de cartas
        self.pile_mat_list.append(pile)

        # Aca estamos creando un sprite a la par del mazo para cuando damos vuelta a una carta
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Creamos las 7 pilas de juego, esto son los sprite estaticos que vemos en pantalla
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Además, creamos 4 más donde van los A, estos de igual forma son los sprite estaticos
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

        # Si la pila que tocamos tiene algo
        if len(cards) > 0:

            primary_card = cards[-1]
            assert isinstance(primary_card, card)

            # Comprueba en que pila está la carta
            pile_index = self.get_pile_for_card(primary_card)

            # Si le damos click al mazo
            if pile_index == BOTTOM_FACE_DOWN_PILE:
                # Nos devuelve tres cartas
                for i in range(3):
                    # Si nos quedamos sin cartas se detiene
                    if len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                        break
                    # Toma la carta de arriba
                    card_aux = self.piles[BOTTOM_FACE_DOWN_PILE][-1]
                    # Le da vuelta
                    card_aux.face_up()

                    card_aux.position = self.pile_mat_list[BOTTOM_FACE_UP_PILE].position
                    # Quita la carta de la pila
                    self.piles[BOTTOM_FACE_DOWN_PILE].remove(card_aux)
                    # Mueve la carta a la pila face up
                    self.piles[BOTTOM_FACE_UP_PILE].append(card_aux)
                    # La pone arriba
                    self.pull_to_top(card_aux)

            elif primary_card.is_face_down:
                # Aca comprobamos que si movemos la ultima carta de una pila esta se va a dar vuelta
                primary_card.face_up()
            else:
                # Los demás casos solo toma la que está para arriba
                self.held_cards = [primary_card]
                # Guarda la posicion
                self.held_cards_original_position = [self.held_cards[0].position]
                # La pone encima
                self.pull_to_top(self.held_cards[0])

                # Toma todas las demás cartas que estamos agarrando
                card_index = self.piles[pile_index].index(primary_card)
                for i in range(card_index + 1, len(self.piles[pile_index])):
                    card_aux = self.piles[pile_index][i]
                    self.held_cards.append(card_aux)
                    self.held_cards_original_position.append(card_aux.position)
                    self.pull_to_top(card_aux)

        else:

            # ¿Le dimos vuelta al mazo y no tiene cartas?
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)

                # Si no tiene cartas
                if mat_index == BOTTOM_FACE_DOWN_PILE and len(self.piles[BOTTOM_FACE_DOWN_PILE]) == 0:
                    # Le da vuelta al mazo e inicia nuevamente
                    temp_list = self.piles[BOTTOM_FACE_UP_PILE].copy()
                    for card_aux in reversed(temp_list):
                        card_aux.face_down()
                        self.piles[BOTTOM_FACE_UP_PILE].remove(card_aux)
                        self.piles[BOTTOM_FACE_DOWN_PILE].append(card_aux)
                        card_aux.position = self.pile_mat_list[BOTTOM_FACE_DOWN_PILE].position

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):

        if len(self.held_cards) == 0:  # Esto comprueba si estamos agarrando alguna carta
            return  # Si no estamos agarrando nada lo dejamos asi

        # Busca la pila más cercana
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        if arcade.check_for_collision(self.held_cards[0], pile):  # Comprueba si tocamos alguna pila, ESTO ES IMPORTANTE

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

                    if self.held_cards[0].value == "K":
                        # Si no hay cartas en esa posicion
                        for i, dropped_card in enumerate(self.held_cards):
                            # Mueve las cartas
                            dropped_card.position = pile.center_x, \
                                                    pile.center_y - CARD_VERTICAL_OFFSET * i
                    else:
                        pass

                for card_aux in self.held_cards:
                    # Movemos la carta a la pila correcta
                    self.move_card_to_new_pile(card_aux, pile_index)

                # No resetee su posicion
                reset_position = False

            # En caso de que queramos mover cartas a las pilas de arriba
            elif TOP_PILE_1 <= pile_index <= TOP_PILE_4 and len(self.held_cards) == 1:

                if self.held_cards[0].value == "A":

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

    def deal_cards(self):
        # Este metodo nos permite agarrar varias cartas a la vez y moverlas

        for pile_no in range(PLAY_PILE_1, PLAY_PILE_7 + 1):

            for j in range(pile_no - PLAY_PILE_1 + 1):

                # Quita la carta de la pila que estamos tocando
                card_aux = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
                # La pone en la pila correcta
                self.piles[pile_no].append(card_aux)
                # Ahora si mueve el sprite a la pila que seleccionamos
                card_aux.position = self.pile_mat_list[pile_no].position
                # La pone arriba
                self.pull_to_top(card_aux)

    def flip_up_top_cards(self):

        for i in range(PLAY_PILE_1, PLAY_PILE_7 + 1):  # Aca empezamos a recorrer todas las pilas de juego
            self.piles[i][-1].face_up()  # Y tomamos la carta de abajo y le damos vuelta boca arriba

    def on_key_press(self, symbol: int, modifiers: int):
        # Esto detecta que si presionamos la tecla R, el juego se va a reiniciar
        if symbol == arcade.key.R:
            # Restart
            self.setup()


def main():
    window = solitaire()  # Declaramos nuestro main y hacemos los respectivos llamados
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
