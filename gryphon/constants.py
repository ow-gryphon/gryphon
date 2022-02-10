from pathlib import Path


BACK = "back"
TYPING = "type"
NODE = "node"
LEAF = "leaf"

SEARCH_BY_KEYWORD = "Search by keyword"
METHODOLOGY = "Methodology"
USE_CASES = "Use-cases"
TOPIC = "Navigate by Topic"
SECTOR = "Navigate by Sector"

# commands
QUIT = "quit"
GENERATE = "generate"
INIT = "init"
ADD = "add"
ABOUT = "about"
SETTINGS = "settings"

# tree related
CHILDREN = "children"
NAME = "name"
VALUE = "value"
SHORT_DESC = "short_description"
LONG_DESC = "long_description"
REFERENCE_LINK = "reference_link"

YES = "yes"
NO = "no"

VENV = ".venv"
SUCCESS = 21
DEFAULT_ENV = "venv"

GRYPHON_HOME = Path.home() / ".gryphon"
PACKAGE_PATH = Path(__file__).parent
DATA_PATH = PACKAGE_PATH / "data"
CONFIG_FILE = GRYPHON_HOME / "gryphon_config.json"
DEFAULT_CONFIG_FILE = DATA_PATH / "gryphon_config.json"
