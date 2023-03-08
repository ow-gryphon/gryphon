from ..functions import erase_lines, BackSignal
from ...fsm import State


class MainMenu(State):
    name = "main_menu"
    transitions = []

    def on_start(self, _: dict):
        erase_lines(n_lines=2)
        raise BackSignal()
