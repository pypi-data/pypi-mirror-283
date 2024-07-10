import json
import os
import sys

import jsonschema
from jsonschema import validate

from data_processing_flows import Flow
from data_processing.utils import get_logger

logger = get_logger(__name__)


def generate_flow(config_file: str) -> Flow:
    """
    Loads a flow JSON definition from a given file, validates its schema and creates a Flow object

    :param config_file: a JSON file with flow definition
    :return: a Flow object
    """
    # Load the flow JSON schema
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "flow_schema.json")), "r") as file:
        flow_schema = json.load(file)
    # Load the flow definition
    with open(config_file) as json_file:
        flow_def = json.load(json_file).get("flow")
    # Validate the flow definition
    try:
        validate(instance=flow_def, schema=flow_schema)
        logger.info(f"Flow configuration from the {config_file} file is valid")
    except jsonschema.exceptions.ValidationError as err:
        logger.error(f"Flow configuration from the {config_file} file is invalid: {err.message}")
        sys.exit(1)

    flow = Flow(
        name=flow_def.get("name", ""),
        description=flow_def.get("description", ""),
        global_params=flow_def.get("global_parameters", {}),
    )
    for step in flow_def.get("steps", []):
        config_class = step.get("transform_config_class", "")
        clazz = __class_loader(config_class)
        parameters = step.get("parameters", {})
        flow.add_step(clazz(), parameters)
    return flow


# TODO: should it be moved to utils, or some other lib ?
def __class_loader(class_name: str):
    """
        Dynamically load a class according to the defined name.

        :param class_name: the full qualified class name, the string should contain the module name(s) and the class name.
        :return: the loaded class object.
    """

    if class_name == "":
        logger.error("Class is not defined")
        sys.exit(1)
    parts = class_name.rsplit(".", 1)
    if len(parts) == 1:
        logger.error("Module of the class is not defined")
        sys.exit(1)
    try:
        mod = __import__(parts[0])
        clazz = getattr(mod, parts[1])
    except ModuleNotFoundError:
        logger.error(f"Module '{parts[0]}' not found.")
        sys.exit(1)
    except AttributeError:
        logger.error(f"Class '{mod, parts[1]}' not found in module '{parts[0]}'.")
        sys.exit(1)
    return clazz


# used for unit testing only
def main():
    flow = generate_flow(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../test-data/flow_test.json")))
    print(flow)
    flow.execute()


# main entry point into the program; used for unit testing only
if __name__ == "__main__":
    main()
