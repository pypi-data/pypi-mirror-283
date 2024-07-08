import logging
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

log = logging.getLogger(__name__)


def deploy_to_databricks(package_name: str, path: str, env: str, bundle: bool = True):
    if shutil.which("databricks") is None:
        raise Exception("databricks CLI is not installed")

    project_path = Path(path)
    if not project_path.exists():
        raise FileNotFoundError(f"Project path {project_path} does not exist")
    os.chdir(project_path)
    if not (project_path / "databricks.yml").exists():
        raise FileNotFoundError(
            f"Configuration file {project_path / 'databricks.yml'} does not exist"
        )

    _build_project()
    if bundle is True:
        _bundle_project(env)
    _upload_project_config(package_name, project_path)
    _upload_project_data(package_name, project_path)
    deploy_cmd = ["databricks", "bundle", "deploy", "--target", env]
    result = subprocess.run(deploy_cmd, check=True, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Failed to deploy the project: {result.stderr}")
    log.info("Project deployed successfully!")


def _upload_project_data(package_name, project_path):
    log.info("Upload project data to Databricks...")
    data_path = project_path / "data"
    if data_path.exists():
        copy_data_cmd = [
            "databricks",
            "fs",
            "cp",
            "-r",
            str(data_path),
            f"dbfs:/FileStore/{package_name}/data",
        ]
        result = subprocess.run(copy_data_cmd, check=False, capture_output=True)
        if result.returncode != 0:
            raise Exception(f"Failed to copy data to Databricks: {result.stderr}")


def _upload_project_config(package_name, project_path):
    log.info("Upload project configuration to Databricks...")
    with tarfile.open(project_path / f"dist/conf-{package_name}.tar.gz") as f:
        f.extractall("dist/")

    try:
        remove_cmd = ["databricks", "fs", "rm", "-r", f"dbfs:/FileStore/{package_name}"]
        result = subprocess.run(remove_cmd, check=False)
        if result.returncode != 0:
            log.warning(f"Failed to remove existing project: {result.stderr}")
    except Exception as e:
        log.warning(f"Failed to remove existing project: {e}")

    conf_path = project_path / "dist" / "conf"
    if not conf_path.exists():
        raise FileNotFoundError(f"Configuration path {conf_path} does not exist")

    copy_conf_cmd = [
        "databricks",
        "fs",
        "cp",
        "-r",
        str(conf_path),
        f"dbfs:/FileStore/{package_name}/conf",
    ]
    result = subprocess.run(copy_conf_cmd, check=False, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Failed to copy configuration to Databricks: {result.stderr}")


def _bundle_project(env):
    log.info("Bundling the project...")
    bundle_cmd = ["kedro", "databricks", "bundle", "--env", env]
    result = subprocess.run(bundle_cmd, capture_output=True, check=True)
    if result.returncode != 0:
        raise Exception(f"Failed to bundle the project: {result.stderr}")


def _build_project():
    log.info("Building the project...")
    build_cmd = ["kedro", "package"]
    result = subprocess.run(build_cmd, capture_output=True, check=True)
    if result.returncode != 0:
        raise Exception(f"Failed to build the project: {result.stderr}")


if __name__ == "__main__":
    deploy_to_databricks()
