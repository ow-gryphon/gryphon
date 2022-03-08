from typing import List
from .state import State


class FSM:

    def __init__(self, initial_state: State, state_collection: List[State]):
        self.current_state = initial_state
        self.states = state_collection
        self.history = [initial_state]

    def run_interaction(self, *args, **kwargs):
        args, kwargs = self.current_state.on_start(*args, **kwargs)
        transition = self.current_state.check_transitions(*args, **kwargs)

        self.current_state = transition.next_state
        self.history.append(self.current_state)

    def run(self):
        while not self.current_state.is_final_state:
            self.run_interaction()
