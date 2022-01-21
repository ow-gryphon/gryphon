import platform
from gryphon.wizard.wizard_text import Text
from .constants import KEY_DOWN, WELCOME_MESSAGE, CONFIRMATION_MESSAGE, SUCCESS_MESSAGE

if platform.system() != "Windows":
    import pexpect
else:
    # noinspection PyUnresolvedReferences
    import wexpect as pexpect


def wizard_add_typing(lib_name):

    child = pexpect.spawn(command=f'gryphon')

    # » Install Python libraries/packages
    child.expect(WELCOME_MESSAGE)
    child.send(KEY_DOWN * 2)
    child.sendcontrol('m')

    # » ○ >> Type the library name manually
    child.expect(Text.add_prompt_categories_question)
    child.send(KEY_DOWN * 8)
    child.sendcontrol('m')

    child.expect(Text.add_prompt_type_library)
    child.send(lib_name)
    child.sendcontrol('m')

    child.expect(CONFIRMATION_MESSAGE)
    child.sendcontrol('m')

    child.expect(SUCCESS_MESSAGE)
    child.close()


def wizard_add_matplotlib():

    child = pexpect.spawn(command='gryphon')

    # » Install Python libraries/packages
    child.expect(WELCOME_MESSAGE)
    child.send(KEY_DOWN * 2)
    child.sendcontrol('m')

    # » ○ >> Data Visualization
    child.expect(Text.add_prompt_categories_question)
    child.sendcontrol('m')

    # » ○ >> matplotlib
    child.expect(Text.add_prompt_categories_question)
    child.sendcontrol('m')

    child.expect(CONFIRMATION_MESSAGE)
    child.sendcontrol('m')

    child.expect(SUCCESS_MESSAGE)
    child.close()
