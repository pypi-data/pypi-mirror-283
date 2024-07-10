import os
import sys
import time
import timeit
from typing import Any

from data_processing.data_access import DataAccessFactory
from data_processing.runtime import TransformRuntimeConfiguration
from data_processing.utils import get_logger
from data_processing.runtime.pure_python import (
    PythonTransformLauncher,
    PythonTransformRuntimeConfiguration,
)
from data_processing.utils import ParamsUtils
from data_processing_ray.runtime.ray import (
    RayTransformLauncher,
    RayTransformRuntimeConfiguration,
)

logger = get_logger(__name__)


class Flow:
    """
    Define a partial order of transformer execution, can be called workflow or pipeline too.
    """

    def __init__(
            self, *, name: str = "", description: str = "", use_virtual_env: bool = False,
            global_params: dict[str:Any] = {}
    ):
        """
        Create a data processing flow.
        :param name: the flow name
        :param description: the flow description
        :param global_params: a dictionary of parameters which are shared among all flow steps. Individual steps are
        able to overwrite global parameters
        :param use_virtual_env" future support of dynamically updated python environment.
        """
        self.name = name
        self.description = description
        self.data_access_factory = DataAccessFactory()
        self.steps = []
        self.use_virtual_env = use_virtual_env
        self.global_params = global_params

    def add_step(self, transform_config: TransformRuntimeConfiguration, step_params: dict[str:Any]):
        """
        Adds the next flow step

        :param transform_config: the transformer configuration of the step :param step_params: the dictionary of the
        step parameters. These parameters will be merged with the flow global parameters, when the step parameters
        overwrite correspondent global parameters.
        """
        self.steps.append(FlowStep(transform_config=transform_config, step_params=step_params))
        logger.debug("added FlowStep with {type(transform_config).__name__} and parameters {step_params}")

    def __prepare_launch(self):
        """
            Updates the input and output folders of the flow steps, so the output folder of the step 'n' will be the
            input folder of the step 'n+1'. Outputs of the steps are generated in the 'intermediate' folder which is
            defined in the flow global parameters plus the step name
            There are 2 special cases:
            - the input of the first step is the 'input' of the flow from its global parameters.
            - the output of the last step is the 'output' of the flow from its global parameters.

            Finally, the method converts steps parameters from a dictionary to a list of request arguments.
        """
        global_data_conf = self.global_params.get("data_local_config")  # TODO add S3
        intermediate_folder = global_data_conf.get("intermediate_folder")
        for i in range(len(self.steps)):
            if i == 0:
                # the first flow step
                input_folder = global_data_conf.get("input_folder")
            else:
                input_folder = os.path.join(intermediate_folder, self.steps[i - 1].transform_config.get_name())
            if i + 1 == len(self.steps):
                # the last flow step
                output_folder = global_data_conf.get("output_folder")
            else:
                output_folder = os.path.join(intermediate_folder, self.steps[i].transform_config.get_name())
            local_conf = {
                "input_folder": input_folder,
                "output_folder": output_folder,
            }
            self.steps[i].step_params["data_local_config"] = local_conf
            self.steps[i].params_list = ParamsUtils.prepare_parameters(self.global_params, self.steps[i].step_params)

    def __str__(self) -> str:
        class_name = type(self).__name__
        return_str = (
                f"{class_name}( Name: {self.name}, Description: {self.description}\n"
                + f"  Global params={self.global_params}\n"
        )
        if len(self.steps) > 0:
            return_str += "\n  Steps:"
            for step in self.steps:
                return_str += f"\n\t{str(step)}"
        else:
            return_str += "\nSteps:{}"
        return return_str

    def execute(self):
        """
        Execute the flow
        """
        self.__prepare_launch()

        flow_start = time.time()
        for step in self.steps:
            org_argv = sys.argv
            sys.argv = step.params_list
            step_start = time.time()
            logger.info(f"start step {step.transform_config.get_name()} with params = {step.params_list}")
            if isinstance(step.transform_config, RayTransformRuntimeConfiguration):
                launcher = RayTransformLauncher(runtime_config=step.transform_config)
            elif isinstance(step.transform_config, PythonTransformRuntimeConfiguration):
                launcher = PythonTransformLauncher(runtime_config=step.transform_config)
            else:
                logger.error(f"Unrecognizable type of TransformRuntimeConfiguration - {type(step.transform_config)}")
                sys.exit(1)
            launcher.launch()
            sys.argv = org_argv
            logger.info(
                f"the '{step.transform_config.get_name()}' step finished, it took {time.time() - step_start} sec")
        logger.info(f" the flow {self.name} successfully finished in {time.time() - flow_start} sec")


class FlowStep:
    """
    A particular step of the flow execution
    """

    def __init__(self, transform_config: TransformRuntimeConfiguration, step_params: dict[str:Any]):
        self.params_list = None
        self.transform_config = transform_config
        self.step_params = step_params

    def __str__(self) -> str:
        return f"Configuration {type(self.transform_config).__name__}, Parameters: {self.step_params}"
