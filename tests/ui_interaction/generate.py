import platform
from gryphon.wizard.wizard_text import Text
from .constants import KEY_DOWN, WELCOME_MESSAGE, CONFIRMATION_MESSAGE, SUCCESS_MESSAGE

if platform.system() != "Windows":
    import pexpect
else:
    # noinspection PyUnresolvedReferences
    import wexpect as pexpect


def wizard_generate():
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
    child.send(KEY_DOWN)
    child.sendcontrol('m')

    #  » Regression and Classification modeling for NCT
    child.expect(Text.generate_prompt_template_question)
    child.sendcontrol('m')

    # Confirm to proceed
    child.expect(CONFIRMATION_MESSAGE)
    child.sendcontrol('m')

    child.expect(SUCCESS_MESSAGE)
    child.close()
