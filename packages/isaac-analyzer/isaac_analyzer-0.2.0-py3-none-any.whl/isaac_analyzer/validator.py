from isaac_analyzer.logging import getLogger
from isaac_analyzer.yaml_loader import load_yaml
import json
import jsonschema
from jsonschema import Draft202012Validator
from importlib.resources import files

logger = getLogger(__name__)


def load_schema(schema_path):
    logger.debug(f"Loading schema at: {schema_path}")
    with files("isaac_analyzer").joinpath(schema_path).open() as file:
        return json.load(file)


def validate_yaml(file_path, schema_path):
    logger.info(f"Validating {file_path}")
    schema = load_schema(schema_path)
    logger.debug("Schema loaded")

    data = load_yaml(file_path)
    logger.debug("Yaml file loaded.")
    validator = Draft202012Validator(schema)

    try:
        validator.validate(data)
        logger.info("YAML file is valid.")
    except jsonschema.exceptions.ValidationError as err:
        for error in sorted(validator.iter_errors(data), key=str):
            logger.error(
                f"YAML file is invalid: {error.message} at {[ x + 1 if isinstance(x, int) else x for x in list(error.path)]}"
            )
        raise err
