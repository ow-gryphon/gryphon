from pathlib import Path


# commands
QUIT = "quit"
GENERATE = "generate"
INIT = "init"
DOWNLOAD = "download"
INIT_FROM_EXISTING = "init_from_existing"
DOWNLOAD = "download"
ADD = "add"
HANDOVER = "handover"
ABOUT = "about"
CONFIGURE_PROJECT = "configure_project"
FEEDBACK = "feedback"
REPORT_BUG = "report_bug"
SETTINGS = "settings"
CONTACT_US = "contact_us"

# tree related
NODE = "node"
LEAF = "leaf"
CHILDREN = "children"
NAME = "name"
VALUE = "value"

# add tree
SHORT_DESC = "short_description"
LONG_DESC = "long_description"
REFERENCE_LINK = "reference_link"

# generate tree
SEARCH_BY_KEYWORD = "Search by keyword"
METHODOLOGY = "Methodology"
USE_CASES = "Use-cases"
TOPIC = "Navigate by Topic"
SECTOR = "Navigate by Sector"
TYPING = "type"

# choices
YES = "yes"
NO = "no"
BACK = "back"
READ_MORE = "read_more"
CHANGE_LOCATION = "change_location"
TYPE_AGAIN = "type_again"
SPECIFY_VERSION = "specify_version"

# log
SUCCESS = 21

# environment
VENV_FOLDER = ".venv"
CONDA_FOLDER = "envs"
DEFAULT_ENV = "venv"
VENV = "venv"
CONDA = "conda"

# path
GRYPHON_HOME = Path.home() / ".gryphon"
PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "data"
CONFIG_FILE = GRYPHON_HOME / "gryphon_config.json"
DEFAULT_CONFIG_FILE = DATA_PATH / "gryphon_config.json"
REQUIREMENTS = "requirements.txt"

# Python versions
DEFAULT_PYTHON_VERSION = "3.8"
ALWAYS_ASK = "always_ask"
USE_LATEST = "use_latest"
LATEST = "LATEST"
SYSTEM_DEFAULT = "system_default"
MIN_MAJOR_VERSION = 3
MIN_MINOR_VERSION = 7


REMOTE_INDEX = "remote_index"
LOCAL_TEMPLATE = "local"
GRYPHON_RC = ".gryphon_rc"
PRE_COMMIT_YML = '.pre-commit-config.yaml'
CHANGE_LIMIT = "CHANGE_LIMIT"

ERASE_LINE = "\033[A                                                                                             " \
             "          \033[A"

# addon options
NB_EXTENSIONS = "nbextensions"
NB_STRIP_OUT = "nbstripout"
PRE_COMMIT_HOOKS = "hooks"
CI_CD = "cicd"

ADDON_NAME_MAPPING = {
    NB_EXTENSIONS: "Notebook extensions",
    NB_STRIP_OUT: "Notebook stripout",
    PRE_COMMIT_HOOKS: "Pre-commit hooks",
    CI_CD: "CI/CD"
}

EMAIL_RECIPIENT = "OWGryphonSupport@mmcglobal.onmicrosoft.com"
EMAIL_RECIPIENT_CC = "daniel.uken@oliverwyman.com; daniel.wang@oliverwyman.com"