from ..questions import GenerateQuestions
from ...fsm import Transition, State, negate_condition


def filter_by_keyword(keyword_to_find, templates):
    if keyword_to_find not in ['', ' ']:
        return {
            name: template
            for name, template in templates.items()
            if keyword_to_find.lower() in '\t'.join(template.keywords).lower()
        }
    return []


def _condition_nothing_found(context: dict) -> bool:
    return not bool(len(context["filtered_templates"]))


class AskKeyword(State):
    name = "ask_keyword"
    transitions = [
        Transition(
            next_state="nothing_found",
            condition=_condition_nothing_found
        ),
        Transition(
            next_state="ask_template",
            condition=negate_condition(_condition_nothing_found)
        )
    ]

    def on_start(self, context: dict) -> dict:
        keyword = GenerateQuestions.generate_keyword_question()
        context["filtered_templates"] = filter_by_keyword(keyword, context["templates"])
        return context
