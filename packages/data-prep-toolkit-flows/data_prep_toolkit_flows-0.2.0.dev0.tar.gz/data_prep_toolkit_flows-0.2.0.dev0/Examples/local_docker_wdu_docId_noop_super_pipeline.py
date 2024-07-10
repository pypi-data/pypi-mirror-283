from kfp.dsl import Artifact, Input, Output

from kfp import dsl, local


local.init(runner=local.DockerRunner())


@dsl.component(base_image="quay.io/dataprep1/data-prep-kit/wdu-ray:0.2.1.dev0")
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
        "data_files_to_use": ast.literal_eval("['.zip']"),
    }
    sys.argv = ParamsUtils.dict_to_req(d=params)
    # create launcher
    launcher = PythonTransformLauncher(WduPdf2MdTransformPythonConfiguration())
    # launch
    launcher.launch()


@dsl.component(base_image="quay.io/dataprep1/data-prep-kit/doc_id-ray:0.2.0")
def doc_id(input_folder: Input[Artifact], output_folder: Output[Artifact], input_params: dict):
    import sys

    from data_processing.utils import ParamsUtils
    from data_processing_ray.runtime.ray import RayTransformLauncher
    from doc_id_transform_ray import DocIDRayTransformConfiguration

    local_conf = {
        "input_folder": input_folder.path,
        "output_folder": output_folder.path,
    }
    worker_options = {"num_cpus": 0.8}
    params = input_params | {
        "data_local_config": ParamsUtils.convert_to_ast(local_conf),
        "run_locally": True,
        "runtime_worker_options": ParamsUtils.convert_to_ast(worker_options),
        "runtime_num_workers": 3,
        # doc id configuration
        "doc_id_doc_column": "contents",
        "doc_id_hash_column": "hash_column",
        "doc_id_int_column": "int_id_column",
    }
    sys.argv = ParamsUtils.dict_to_req(d=params)
    # create launcher

    launcher = RayTransformLauncher(DocIDRayTransformConfiguration())
    # launch
    launcher.launch()


@dsl.component(base_image="quay.io/dataprep1/data-prep-kit/noop-ray:0.2.0")
def noop(input_folder: Input[Artifact], output_folder: Output[Artifact], input_params: dict):
    import sys

    from data_processing.runtime.pure_python import PythonTransformLauncher
    from data_processing.utils import ParamsUtils
    from noop_transform_python import NOOPPythonTransformConfiguration

    # create parameters
    local_conf = {
        "input_folder": input_folder.path,
        "output_folder": output_folder.path,
    }
    params = input_params |  {
        "data_local_config": ParamsUtils.convert_to_ast(local_conf),
        # noop params
        "noop_sleep_sec": 1,
    }

    sys.argv = ParamsUtils.dict_to_req(d=params)
    # create launcher
    launcher = PythonTransformLauncher(runtime_config=NOOPPythonTransformConfiguration())
    # Launch the ray actor(s) to process the input
    launcher.launch()


@dsl.pipeline
def wdu_test_pipeline(
    input_folder_path: str = "/home/dpk/test-data/input",
    # output_folder_path: str = "/home/dpk/test-data/super-output",
    runtime_code_location: str = "{'github': 'github', 'commit_hash': '12345', 'path': 'path'}",
    runtime_pipeline_id: str = "pipeline_id",
    runtime_job_id: str = "job_id",
):
    args = locals()
    args.pop("input_folder_path", "")
    args.pop("output_folder_path", "")
    wdu_task = wdu(input_folder=input_folder_path, input_params=args)
    doc_id_task = doc_id(input_folder=wdu_task.outputs["output_folder"], input_params=args)
    noop_task = noop(
        input_folder=doc_id_task.outputs["output_folder"], input_params=args
    )

pipeline_task = wdu_test_pipeline()
