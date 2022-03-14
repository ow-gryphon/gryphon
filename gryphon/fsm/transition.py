def negate_condition(condition: callable):
    def _f(context):
        return not condition(context)

    return _f


def dummy(context: dict) -> dict:
    return context


class Transition:
    def __init__(self, next_state: object, condition: callable, callback: callable = dummy):
        self.next_state = next_state
        self.condition = condition
        self.callback = callback

    def check_condition(self, context):
        transition = self.condition(context)
        assert isinstance(transition, bool)
        return transition


