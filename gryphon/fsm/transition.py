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

        if not isinstance(transition, bool):
            raise RuntimeError(f"Wrong transition return type. "
                               f"Next state: {self.next_state} "
                               f"Returned: {transition} "
                               f"Return type: {type(transition)} "
                               f"Expected: Bool")
        return transition


