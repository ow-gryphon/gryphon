from ..functions import erase_lines
from ..questions import SettingsQuestions
from ...constants import NO, YES, CHANGE_LOCATION, NB_STRIP_OUT, CI_CD, PRE_COMMIT_HOOKS
from ...core.template_scaffolding import template_scaffolding
from ...fsm import State, Transition


def back_to_previous(history, **kwargs):
    history.pop()
    erase_lines(**kwargs)


#####
def _condition_from_new_template_to_end(context: dict) -> bool:
    return context["confirmation_option"] == YES


def _callback_from_new_template_to_end(context: dict) -> dict:
    template_scaffolding(
        context["location"],
        install_nb_strip_out=NB_STRIP_OUT in context["selected_addons"],
        install_ci_cd=CI_CD in context["selected_addons"],
        install_pre_commit_hooks=PRE_COMMIT_HOOKS in context["selected_addons"]
    )

    context["history"] = []
    print("\n")
    return context


#####
def _condition_from_new_template_to_new_template(context: dict) -> bool:
    return context["confirmation_option"] == CHANGE_LOCATION


def _callback_from_new_template_to_new_template(context: dict) -> dict:
    erase_lines(n_lines=3)
    return context


####
def _condition_from_new_template_to_ask_option(context: dict) -> bool:
    return context["confirmation_option"] == NO


def _callback_from_from_new_template_to_ask_option(context: dict) -> dict:
    # remove 2 entries from history
    back_to_previous(context["history"], n_lines=2)
    back_to_previous(context["history"], n_lines=2)
    return context


class NewTemplate3(State):
    name = "new_template3"
    transitions = [
        Transition(
            next_state="ask_option",
            condition=_condition_from_new_template_to_ask_option,
            callback=_callback_from_from_new_template_to_ask_option
        ),
        Transition(
            next_state="ask_option",
            condition=_condition_from_new_template_to_end,
            callback=_callback_from_new_template_to_end
        ),
        Transition(
            next_state="perform_action",
            condition=_condition_from_new_template_to_new_template,
            callback=_callback_from_new_template_to_new_template
        )
    ]

    def on_start(self, context: dict) -> dict:
        context["confirmation_option"] = SettingsQuestions.confirm_new_template(context["location"])

        return context
