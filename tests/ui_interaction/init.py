import platform
from gryphon.wizard.wizard_text import Text
from .constants import KEY_DOWN, WELCOME_MESSAGE, CONFIRMATION_MESSAGE, SUCCESS_MESSAGE


if platform.system() != "Windows":
    import pexpect
else:
    # noinspection PyUnresolvedReferences
    import wexpect as pexpect


def wizard_init(project_folder):
    child = pexpect.spawn(command='gryphon', encoding='utf-8')

    child.expect(WELCOME_MESSAGE)
    #  » Start a new project
    child.sendcontrol('m')

    child.expect(Text.init_prompt_template_question)
    child.send(KEY_DOWN)
    #   Basic analytics template
    #  » Advanced analytics template
    child.sendcontrol('m')

    child.expect(Text.init_prompt_location_question)
    child.send(project_folder)
    child.sendcontrol('m')

    child.expect(CONFIRMATION_MESSAGE)
    child.sendcontrol('m')

    child.expect(SUCCESS_MESSAGE)
    child.close()
