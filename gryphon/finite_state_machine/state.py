from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from .transition import Transition


class State(ABC):

    def __init__(self, name: str, transitions: List[Transition]):
        self.name = name
        self.transitions = transitions
        self.is_final_state = not len(self.transitions)

    @abstractmethod
    def on_start(self, *args, **kwargs) -> Tuple[List, Dict]:
        pass

    @abstractmethod
    def on_transition(self, *args, **kwargs) -> Tuple[List, Dict]:
        pass

    def check_transitions(self, *args, **kwargs) -> Transition:
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

        return transition_passed
