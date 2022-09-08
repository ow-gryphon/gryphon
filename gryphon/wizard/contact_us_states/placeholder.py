from ...fsm import State


class Placeholder(State):
    name = "placeholder"
    transitions = []

    def on_start(self, context: dict) -> dict:
        return context
