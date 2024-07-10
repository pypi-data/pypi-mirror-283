from kfp.dsl import Artifact, Input, Output

from kfp import dsl, local


local.init(runner=local.SubprocessRunner(use_venv=False))


@dsl.component()
def wdu(input_folder: str, output_folder: Output[Artifact], input_params: dict):
    import ast
    import sys

    from data_processing.runtime.pure_python import PythonTransformLauncher
    from data_processing.utils import ParamsUtils
    from wdu_pdf2md_transform_python import WduPdf2MdTransformPythonConfiguration

    local_conf = {
        "input_folder": input_folder,
        "output_folder": output_folder.path,
    }

    params = input_params | {
        # Data access. Only required parameters are specified
        "data_local_config": ParamsUtils.convert_to_ast(local_conf),
        "data_files_to_use": ast.literal_eval("['.pdf']"),
    }
    sys.argv = ParamsUtils.dict_to_req(d=params)
    # create launcher
    launcher = PythonTransformLauncher(WduPdf2MdTransformPythonConfiguration())
    # launch
    launcher.launch()


@dsl.component(base_image="docker.io/python:3.10.14-slim-bullseye")
def resize(input_folder: Input[Artifact], output_folder: str, input_params: dict):
    import sys

    from data_processing.runtime.pure_python import PythonTransformLauncher
    from data_processing.utils import ParamsUtils
    from resize_transform_python import ResizePythonTransformConfiguration

    # create parameters
    local_conf = {
        "input_folder": input_folder.path,
        "output_folder": output_folder,
    }
    params = {
        "data_local_config": ParamsUtils.convert_to_ast(local_conf),
        # resize params
        "resize_max_rows_per_table": 125,
    }
    sys.argv = ParamsUtils.dict_to_req(d=params)
    # create launcher
    launcher = PythonTransformLauncher(runtime_config=ResizePythonTransformConfiguration())
    # launch
    launcher.launch()


@dsl.pipeline
def wdu_test_pipeline(
    input_folder_path: str = "../../test-data/input/wdu_pdf2md/",
    output_folder_path: str = "../test-data/super-output_wdu_pdf2md/",
    runtime_code_location: str = "{'github': 'github', 'commit_hash': '12345', 'path': 'path'}",
    runtime_pipeline_id: str = "pipeline_id",
    runtime_job_id: str = "job_id",
):
    args = locals()
    args.pop("input_folder_path", "")
    args.pop("output_folder_path", "")
    wdu_task = wdu(input_folder=input_folder_path, input_params=args)
    resize_task = resize(input_folder=wdu_task.outputs["output_folder"],output_folder=output_folder_path,  input_params=args)

pipeline_task = wdu_test_pipeline()
