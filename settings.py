import os

DEBUG = True

ADDR = ("127.0.0.1", 8000)

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = ROOT_DIR + "/templates/"

DATABASE_URL = "postgresql://localhost:5432/wblog"
#DATABASE_URL = os.environ.get("DATABASE_URL") + "wblog"
