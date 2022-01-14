from gryphon.wizard.wizard_text import Text
from .constants import *


def wizard_generate(file_name):
    child = pexpect.spawn(command='gryphon')

    # » Load template code into an existing project
    child.expect(WELCOME_MESSAGE)
    child.send(KEY_DOWN)
    child.sendcontrol('m')

    child.expect(Text.add_prompt_categories_question)
    child.sendcontrol('m')

    child.expect(Text.add_prompt_categories_question)
    child.sendcontrol('m')

    child.expect(Text.generate_prompt_template_question)
    child.sendcontrol('m')

    child.expect('Name for the problem')
    child.send(file_name)
    child.sendcontrol('m')

    child.expect(CONFIRMATION_MESSAGE)
    child.sendcontrol('m')

    child.expect(SUCCESS_MESSAGE)
    child.close()
