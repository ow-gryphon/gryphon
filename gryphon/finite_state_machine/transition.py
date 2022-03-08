from .state import State


class Transition:
    def __init__(self, origin: State, next_state: State, condition: callable):
        self.origin = origin
        self.next_state = next_state
        self.condition = condition

    def check_condition(self, *args, **kwargs):
        transition = self.condition(*args, **kwargs)
        assert isinstance(transition, bool)
        return transition
