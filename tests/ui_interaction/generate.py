import platform
from gryphon.wizard.wizard_text import Text
from .constants import KEY_DOWN, WELCOME_MESSAGE, CONFIRMATION_MESSAGE, SUCCESS_MESSAGE

if platform.system() != "Windows":
    import pexpect
else:
    # noinspection PyUnresolvedReferences
    import wexpect as pexpect


def wizard_generate(file_name):
    child = pexpect.spawn(command='gryphon')

    # » Load template code into an existing project
    child.expect(WELCOME_MESSAGE)
    child.send(KEY_DOWN)
    child.sendcontrol('m')

    # Methodology
    child.expect(Text.add_prompt_categories_question)
    child.sendcontrol('m')

    # Classification
    child.expect(Text.add_prompt_categories_question)
    child.sendcontrol('m')

    # Placeholder
    child.expect(Text.generate_prompt_template_question)
    child.sendcontrol('m')

    child.expect('Name for the clustering problem')
    child.send(file_name)
    child.sendcontrol('m')

    child.expect(CONFIRMATION_MESSAGE)
    child.sendcontrol('m')

    child.expect(SUCCESS_MESSAGE)
    child.close()
