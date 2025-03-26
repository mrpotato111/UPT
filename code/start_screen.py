from ursina import *


class Start_Screen(Entity):
    def __init__(self, tut_bol_change):
        super().__init__(parent=camera.ui)

        self.tutorial = tut_bol_change

        self.title = Text(text="Supermarket Simulaator", scale=2, origin=(0, 0.5), y=0.2, parent=self)

        self.start_button = Button(text="Start", scale=(0.2, 0.1), y=-0.1, parent=self)
        self.start_button.on_click = self.start_game

        self.Tutorial_button = Button(text="Tutorial", scale=(0.2, 0.1), y=-0.2, parent=self)
        self.Tutorial_button.on_click = self.start_tutorial

        self.end_button = Button(text="Quit", scale=(0.2, 0.1), y=-0.3, parent=self)
        self.end_button.on_click = self.end_game

    def start_game(self):
        invoke(destroy, self, delay=0)

    def start_tutorial(self):
        self.start_tutorial = True
        self.tutorial()
        invoke(destroy, self, delay=0)
        return self.start_tutorial

    def end_game(self):
        quit()


class End_screen(Entity):
    def __init__(self, reset_funct, answer):
        super().__init__(parent=camera.ui)

        self.reset = reset_funct

        self.title = Text(text="Game Over\n"
                               f"\nright answer was {answer}", scale=2, origin=(0, 0.5), y=0.2, parent=self)

        self.restart_button = Button(text="Restart",scale=(0.2, 0.1), y=-0.1, parent=self)
        self.restart_button.on_click = self.restart_game

        self.end_button = Button(text="Quit", scale=(0.2, 0.1), y=-0.2, parent=self)
        self.end_button.on_click = self.quit_game

    def restart_game(self):
        print("resetting game")
        self.reset()
        invoke(self.destroy_end_screen, delay=0.1)

    def destroy_end_screen(self):
        print("destroying ui")
        self.title.enabled = False
        self.restart_button.enabled = False
        self.end_button.enabled = False
        destroy(self)


    def quit_game(self):
        quit()