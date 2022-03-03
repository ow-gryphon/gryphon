import logging
from questionary import Choice
from ..wizard_text import Text
from ...constants import BACK

logger = logging.getLogger('gryphon')


def base_question(function):
    def _f(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyboardInterrupt:
            logger.warning(f'\nOperation cancelled by user\n')
            exit(0)

    return _f


def get_back_choice():
    return Choice(
        title=Text.back_to_previous_menu_option,
        value=BACK
    )
