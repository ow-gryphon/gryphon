
import platform
if platform.system() != "Windows":
    import pexpect
else:
    # noinspection PyUnresolvedReferences
    import wexpect as pexpect

KEY_UP = '\x1b[A'
KEY_DOWN = '\x1b[B'
KEY_RIGHT = '\x1b[C'
KEY_LEFT = '\x1b[D'

WELCOME_MESSAGE = "Welcome to OW Gryphon"
SUCCESS_MESSAGE = "Installation successful!"
CONFIRMATION_MESSAGE = "Confirm that you want"
