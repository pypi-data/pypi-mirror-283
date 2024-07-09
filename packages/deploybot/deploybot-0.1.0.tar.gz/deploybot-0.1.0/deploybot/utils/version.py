import toml
from pathlib import Path

def get_version():
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject_path, "r") as f:
        pyproject = toml.load(f)
        return pyproject["tool"]["poetry"]["version"]
