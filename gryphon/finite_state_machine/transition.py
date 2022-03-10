
def dummy(*_, **__):
    pass


def negate_condition(condition: callable):
    def _f(*args, **kwargs):
        return not condition(*args, **kwargs)

    return _f


class Transition:
    def __init__(self, next_state: object, condition: callable, callback: callable = dummy):
        self.next_state = next_state
        self.condition = condition
        self.callback = callback

    def check_condition(self, *args, **kwargs):
        transition = self.condition(*args, **kwargs)
        assert isinstance(transition, bool)
        if transition:
            self.callback(*args, **kwargs)
        return transition
