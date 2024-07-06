import yaml
from importlib.resources import files
from isaac_analyzer.logging import getLogger

logger = getLogger(__name__)


def load_yaml(file_path):
    """Load YAML file into a dictionary from a given path."""
    logger.debug(f"Loading YAML file from path: {file_path}")
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        logger.debug(f"Successfully loaded YAML file: {file_path}")
    except Exception as e:
        logger.exception(f"Failed to load YAML file from path: {file_path}, Error: {e}")
    return data


def load_yaml_resource(name):
    """Load YAML file into a dictionary from a resource name."""
    logger.debug(f"Loading YAML resource: {name}")
    try:
        with files("isaac_analyzer").joinpath(f"resources/{name}").open() as file:
            data = yaml.safe_load(file)
        logger.debug(f"Successfully loaded YAML resource: {name}")
    except Exception as e:
        logger.exception(f"Failed to load YAML resource: {name}, Error: {e}")
    return data
