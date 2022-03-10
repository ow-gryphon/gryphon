from abc import ABC, abstractmethod
from typing import List, Tuple, Dict


class State(ABC):

    def __init__(self, name: str, transitions: List):
        self.name = name
        self.transitions = transitions

    @abstractmethod
    def on_start(self, *args, **kwargs) -> Tuple[List, Dict]:
        pass

    def is_final_state(self):
        return not len(self.transitions)

    def check_transitions(self, *args, **kwargs):
        already_transitioned = False
        transition_passed = None
        for t in self.transitions:
            passed = t.check_condition(*args, **kwargs)

            if passed and already_transitioned:
                raise RuntimeError(f"State transitioned simultaneously for more than one state "
                                   f"[{transition_passed.next_state.name}, {t.next_state.name}].")
            elif passed:
                already_transitioned = True
                transition_passed = t

        if not transition_passed:
            raise RuntimeError("State machine halted, no transition conditions were met.")

        return transition_passed
