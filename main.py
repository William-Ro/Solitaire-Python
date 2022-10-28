# Solitaire game, based on https://api.arcade.academy/en/latest/tutorials/card_game/index.html

import arcade


class solitaire(arcade.Window):  # Aca declaramos nuestra clase juego

    def __init__(self):  # Constructor donde declaramos el tamanno de la ventana

        super().__init__(1024, 768, "Solitaire")

        arcade.set_background_color(arcade.color.AMAZON)  # Hacemos la ventana de color verde

    def setup(self):
        pass  # Esto nos sirve para reiniciar el juego

    def clear_screen(self):
        self.clear()

    def on_mouse_press(self, x, y, button, key_modifiers):
        # Esto es para cada vez que un usuario da click nos devuelve la posicion
        pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # Esto es para cada vez que un usuario da click nos devuelve la posicion
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # Esto nos dice cuando el usuario mueve el mouse
        pass


def main():

    window = solitaire()  # Declaramos nuestro main y hacemos los respectivos llamados
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
