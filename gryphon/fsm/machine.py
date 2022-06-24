from ..logger import logger
from ..constants import ERASE_LINE


class HaltSignal(Exception):
    def __init__(self):
        super().__init__()


class Machine:

    def __init__(self, initial_state, possible_states):
        self.history = [initial_state.name]
        self.possible_states = possible_states
        self.current_state = initial_state

    def find_state_by_name(self, name):
        filtered = list(filter(lambda x: name == x.name, self.possible_states))
        if len(filtered):
            return filtered[0]
        else:
            names = [
                p.name
                for p in self.possible_states
            ]
            raise RuntimeError(f"State '{name}' not found in possible states: {names}")

    def run_interaction(self, context: dict):
        context = self.current_state.on_start(context)
        transition = self.current_state.check_transitions(context)

        self.current_state = self.find_state_by_name(transition.next_state)
        logger.debug(f"State: {transition.next_state}")
        if transition is None:
            raise HaltSignal()

        context = transition.callback(context)

        self.history.append(self.current_state.name)
        logger.debug(ERASE_LINE)
        return context

    def run(self):
        context = {}
        while self.current_state and not self.current_state.is_final_state():
            context = self.run_interaction(context)

        self.current_state.on_start(context)
