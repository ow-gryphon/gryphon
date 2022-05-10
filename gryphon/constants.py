from pathlib import Path


# commands
QUIT = "quit"
GENERATE = "generate"
INIT = "init"
ADD = "add"
ABOUT = "about"
SETTINGS = "settings"

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
CHANGE_LOCATION = "change_location"
TYPE_AGAIN = "type_again"
SPECIFY_VERSION = "specify_version"

# log
SUCCESS = 21

# environment
VENV_FOLDER = ".venv"
DEFAULT_ENV = "venv"
VENV = "venv"
CONDA = "conda"

# path
GRYPHON_HOME = Path.home() / ".gryphon"
PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "data"
CONFIG_FILE = GRYPHON_HOME / "gryphon_config.json"
DEFAULT_CONFIG_FILE = DATA_PATH / "gryphon_config.json"

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
