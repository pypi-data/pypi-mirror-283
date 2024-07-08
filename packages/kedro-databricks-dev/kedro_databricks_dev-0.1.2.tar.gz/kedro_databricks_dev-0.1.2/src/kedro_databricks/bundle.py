import copy
import logging
from typing import Any

from kedro.framework.project import PACKAGE_NAME
from kedro.pipeline import Pipeline

from kedro_databricks.utils import (
    TASK_KEY_ORDER,
    WORKFLOW_KEY_ORDER,
    _remove_nulls_from_dict,
    _sort_dict,
)

DEFAULT = "default"

log = logging.getLogger(__name__)


def _create_task(name, depends_on):
    """Create a Databricks task for a given node.

    Args:
        name (str): name of the node
        depends_on (List[Node]): list of nodes that the task depends on

    Returns:
        Dict[str, Any]: a Databricks task
    """
    ## Follows the Databricks REST API schema. See "tasks" in the link below
    ## https://docs.databricks.com/api/workspace/jobs/create

    task = {
        "task_key": name,
        "libraries": [{"whl": "../dist/*.whl"}],
        "depends_on": [{"task_key": dep.name} for dep in depends_on],
        "python_wheel_task": {
            "package_name": PACKAGE_NAME,
            "entry_point": "databricks_run",
            "parameters": [
                "--nodes",
                name,
                "--conf-source",
                f"/dbfs/FileStore/{PACKAGE_NAME}/conf",
                "--package-name",
                PACKAGE_NAME,
            ],
        },
    }

    return _sort_dict(task, TASK_KEY_ORDER)


def _create_workflow(name: str, pipeline: Pipeline):
    """Create a Databricks workflow for a given pipeline.

    Args:
        name (str): name of the pipeline
        pipeline (Pipeline): Kedro pipeline object

    Returns:
        Dict[str, Any]: a Databricks workflow
    """
    ## Follows the Databricks REST API schema
    ## https://docs.databricks.com/api/workspace/jobs/create
    workflow = {
        "name": name,
        "tasks": [
            _create_task(node.name, depends_on=deps)
            for node, deps in pipeline.node_dependencies.items()
        ],
        "format": "MULTI_TASK",
    }

    return _remove_nulls_from_dict(_sort_dict(workflow, WORKFLOW_KEY_ORDER))


def _update_list(old, new, lookup_key, default={}):
    from mergedeep import merge

    old_obj = {curr.pop(lookup_key): curr for curr in old}
    new_obj = {update.pop(lookup_key): update for update in new}
    keys = set(old_obj.keys()).union(set(new_obj.keys()))

    for key in keys:
        update = copy.deepcopy(default)
        update.update(new_obj.get(key, {}))
        new = merge(old_obj.get(key, {}), update)
        old_obj[key] = new

    return [{lookup_key: k, **v} for k, v in old_obj.items()]


def _apply_overrides(workflow, overrides, default_task={}):
    from mergedeep import merge

    workflow["description"] = workflow.get("description", overrides.get("description"))
    workflow["email_notifications"] = merge(
        workflow.get("email_notifications", {}),
        overrides.get("email_notifications", {}),
    )
    workflow["webhook_notifications"] = merge(
        workflow.get("webhook_notifications", {}),
        overrides.get("webhook_notifications", {}),
    )
    workflow["notification_settings"] = merge(
        workflow.get("notification_settings", {}),
        overrides.get("notification_settings", {}),
    )
    workflow["timeout_seconds"] = workflow.get(
        "timeout_seconds", overrides.get("timeout_seconds")
    )
    workflow["health"] = merge(workflow.get("health", {}), overrides.get("health", {}))
    workflow["schedule"] = merge(
        workflow.get("schedule", {}), overrides.get("schedule", {})
    )
    workflow["trigger"] = merge(
        workflow.get("trigger", {}), overrides.get("trigger", {})
    )
    workflow["continuous"] = merge(
        workflow.get("continuous", {}), overrides.get("continuous", {})
    )
    workflow["max_concurrent_runs"] = workflow.get(
        "max_concurrent_runs", overrides.get("max_concurrent_runs")
    )
    workflow["tasks"] = _update_list(
        workflow.get("tasks", []), overrides.get("tasks", []), "task_key", default_task
    )
    workflow["job_clusters"] = _update_list(
        workflow.get("job_clusters", []),
        overrides.get("job_clusters", []),
        "job_cluster_key",
    )
    workflow["git_source"] = merge(
        workflow.get("git_source", {}), overrides.get("git_source", {})
    )
    workflow["tags"] = merge(workflow.get("tags", {}), overrides.get("tags", {}))
    workflow["queue"] = merge(workflow.get("queue", {}), overrides.get("queue", {}))
    workflow["parameters"] = _update_list(
        workflow.get("parameters", []), overrides.get("parameters", []), "name"
    )
    workflow["run_as"] = merge(workflow.get("run_as", {}), overrides.get("run_as", {}))
    workflow["edit_mode"] = workflow.get("edit_mode", overrides.get("edit_mode"))
    workflow["deployment"] = merge(
        workflow.get("deployment", {}), overrides.get("deployment", {})
    )
    workflow["environments"] = _update_list(
        workflow.get("environments", []),
        overrides.get("environments", []),
        "environment_key",
    )
    workflow["access_control_list"] = merge(
        workflow.get("access_control_list", {}),
        overrides.get("access_control_list", {}),
    )
    workflow["format"] = "MULTI_TASK"

    new_workflow = {}
    for k, v in workflow.items():
        if v is None:
            continue
        elif isinstance(v, (dict, list)):
            if len(v) == 0:
                continue
        new_workflow[k] = v

    return new_workflow


def apply_resource_overrides(
    resources: dict, overrides: dict, default_key: str = DEFAULT
):
    default_workflow = overrides.pop(default_key, {})
    try:
        default_task = [
            task
            for task in default_workflow.pop("tasks", [])
            if task.get("task_key") == default_key
        ].pop()
        default_task.pop("task_key")
    except IndexError:
        default_task = {}

    for name, resource in resources.items():
        workflow = resource["resources"]["jobs"][name]
        workflow_overrides = copy.deepcopy(default_workflow)
        workflow_overrides.update(overrides.get(name, {}))
        task_overrides = workflow_overrides.pop("tasks", [])
        try:
            workflow_default_task = [
                task for task in task_overrides if task.get("task_key") == default_key
            ].pop()
            workflow_default_task.pop("task_key")
        except IndexError:
            workflow_default_task = copy.deepcopy(default_task)
        resources[name]["resources"]["jobs"][name] = _apply_overrides(
            workflow, workflow_overrides, default_task=workflow_default_task
        )

    return resources


def generate_resources(
    pipelines: dict[str, Pipeline], package_name=PACKAGE_NAME
) -> dict[str, dict[str, Any]]:
    """Generate Databricks resources for the given pipelines.

    Finds all pipelines in the project and generates Databricks asset bundle resources
    for each according to the Databricks REST API.

    Args:
        pipelines (dict[str, Pipeline]): A dictionary of pipeline names and their Kedro pipelines

    Returns:
        dict[str, dict[str, Any]]: A dictionary of pipeline names and their Databricks resources
    """

    workflows = {}
    for name, pipeline in pipelines.items():
        if len(pipeline.nodes) == 0:
            continue

        wf_name = f"{package_name}_{name}" if name != "__default__" else package_name
        wf = _create_workflow(wf_name, pipeline)
        log.debug(f"Workflow '{wf_name}' created successfully.")
        log.debug(wf)
        workflows[wf_name] = wf

    resources = {
        name: {"resources": {"jobs": {name: wf}}} for name, wf in workflows.items()
    }

    log.info("Databricks resources generated successfully.")
    log.debug(resources)
    return resources
