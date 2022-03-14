
def dummy(*_, **__):
    pass


def negate_condition(condition: callable):
    def _f(context):
        return not condition(context)

    return _f


class Transition:
    def __init__(self, next_state: object, condition: callable, callback: callable = dummy):
        self.next_state = next_state
        self.condition = condition
        self.callback = callback

    def check_condition(self, context):
        transition = self.condition(context)
        assert isinstance(transition, bool)
        if transition:
            self.callback(context)
        return transition
