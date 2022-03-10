from ...finite_state_machine import State
from ..functions import erase_lines, BackSignal


class MainMenu(State):
    name = "main_menu"
    transitions = []

    def __init__(self):
        super().__init__(self.name, self.transitions)

    def on_start(self, *args, **kwargs):
        erase_lines()
        raise BackSignal()
