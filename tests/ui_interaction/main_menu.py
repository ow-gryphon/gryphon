from gryphon.wizard.wizard_text import Text
from .basic_actions import wait_for_output, select_nth_option

NEXT_MENU = "Navigate the categories"
USEFUL_LINKS = "Useful links"


#   ON main menu
#   AND starting on the first option
def select_init_on_main_menu(process):
    select_nth_option(process, n=1)
    wait_for_output(process, Text.init_prompt_template_question)


def select_init_from_existing_on_main_menu(process):
    select_nth_option(process, n=2)
    wait_for_output(process, Text.init_prompt_template_question)


def select_generate_on_main_menu(process):
    select_nth_option(process, n=3)
    wait_for_output(process, Text.add_prompt_categories_question)


def select_add_on_main_menu(process):
    select_nth_option(process, n=4)
    wait_for_output(process, NEXT_MENU)


def select_advanced_on_main_menu(process):
    select_nth_option(process, n=5)
    wait_for_output(process, NEXT_MENU)


def select_about_on_main_menu(process):
    select_nth_option(process, n=6)
    wait_for_output(process, USEFUL_LINKS)


def select_exit_on_main_menu(process):
    select_nth_option(process, n=7)
