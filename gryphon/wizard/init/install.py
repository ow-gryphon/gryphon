from typing import List, Dict, Tuple
from ...finite_state_machine import State
from ...core.init import init as core_init


class Install(State):
    name = "install"
    transitions = []

    def __init__(self):
        super().__init__(self.name, self.transitions)

    def on_start(self, *args, **kwargs) -> Tuple[List, Dict]:
        template = kwargs["template"]
        location = kwargs["location"]
        chosen_version = kwargs["chosen_version"]
        extra_parameters = kwargs["extra_parameters"]

        core_init(
            template=template,
            location=location,
            python_version=chosen_version,
            **extra_parameters
        )

        return list(args), dict(kwargs)
