import ast
import os

from data_processing.utils import ParamsUtils
from data_processing_flows import Flow
from noop_transform_ray import NOOPRayTransformConfiguration
from wdu_pdf2md_transform_python import WduPdf2MdTransformPythonConfiguration


def main():
    code_location = {"github": "github", "commit_hash": "12345", "path": "path"}

    input_folder = os.path.abspath(
        os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../test-data/input/wdu_pdf2md/1_file")))
    )
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test-data/output"))
    intermediate_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test-data/intermediate"))
    local_conf = {
        "input_folder": input_folder,
        "output_folder": output_folder,
        "intermediate_folder": intermediate_folder,
    }
    global_params = {
        "runtime_pipeline_id": "pipeline_id",
        "runtime_job_id": "job_id",
        "runtime_code_location": ParamsUtils.convert_to_ast(code_location),
        "data_local_config": local_conf,
    }

    flow = Flow(name="test", global_params=global_params)
    flow.add_step(
        transform_config=WduPdf2MdTransformPythonConfiguration(),
        step_params={"data_files_to_use": ast.literal_eval("['.zip']")},
    )
    worker_options = {"num_cpus": 0.8}
    noop_step_params = {
        "noop_sleep_sec": 1,
        "run_locally": True,
        "runtime_worker_options": ParamsUtils.convert_to_ast(worker_options),
        "runtime_num_workers": 3,
    }
    flow.add_step(transform_config=NOOPRayTransformConfiguration(), step_params=noop_step_params)
    flow.execute()
    print("Done")


if __name__ == "__main__":
    main()
