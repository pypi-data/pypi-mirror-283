from glob import glob
from os.path import basename, dirname, isfile


def LoadLibs():
    mod_paths = glob(f"{dirname(__file__)}/*.py")
    return sorted([basename(f)[:-3] for f in mod_paths if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")])


for module_name in LoadLibs():
    import_statement = f"from nsdev.{module_name} import *"
    exec(import_statement)
