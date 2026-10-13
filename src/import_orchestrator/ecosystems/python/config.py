"""
Copyright (C) 2026 Lightwell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import os
from pathlib import Path

PYTHON_DEFAULT_DB_PATH = "./python_import_state.db"

# LOCAL SPIKE (KONFLUX-15844) — kflux-lw-p01 / perfscale-3. Do not push.
NAMESPACE = "konflux-perfscale-3-tenant"
PIPELINERUN_PREFIX = "python-remediated-build-"

# Build targets, keyed by target name. Each supplies the Konflux application and
# component labels applied to the PipelineRun, and whether the target produces a
# Release CR (`releases`). Selected via `--target`.
TARGET_CONFIGS: dict[str, dict] = {
    "REMEDIATED": {
        "app": "remediated-build",
        "component": "remediated-build",
        "service_account": "build-pipeline-remediated-build",
    },
    "SCRATCH": {
        "app": "scratch-build",
        "component": "scratch-build",
        "service_account": "build-pipeline-scratch-build",
        "skip_release": True,
        # Clean / probe: run attach-build-index but do not pass --require-vuln
        # (in-cluster Task spike; see pipeline taskRef).
        "require_vuln": False,
    },
}
DEFAULT_TARGET = "SCRATCH"

# Base of the per-package lightwell-builds source repositories. Each package
# lives at "<repo_base>/pypi.org-<package>".
LIGHTWELL_BUILDS_REPO_BASE = "https://gitlab.cee.redhat.com/lightwell/lightwell-builds"

# Spike: full URL (probe source) instead of lightwell/lightwell-builds/pypi.org-*
LIGHTWELL_BUILDS_REPO_URL_OVERRIDE = (
    "https://gitlab.cee.redhat.com/jhutar/lw-pypi.org-ntplib-1"
)

# Spike: full ImageRepository URL (flat). pipelinerun uses this as repo + :tag.
IMAGE_REPO_BASE = (
    "quay.io/redhat-user-workloads/konflux-perfscale-3-tenant/scratch-build"
)

# Spike: reuse probe git-auth secret in this namespace.
GIT_AUTH_SECRET = "probe-build-configs-git-auth"

# Wheel cache server URL pointing to the Lightwell validated Python repository.
WHEEL_SERVER_URL = os.environ.get(
    "WHEEL_SERVER_URL",
    "https://packages.redhat.com/lightwell/python/validated/simple/",
)


def pipeline_definition_path() -> Path:
    """Return the path to the python-remediated-build pipeline definition.

    Configurable via TEKTON_PIPELINE_DIR; otherwise falls back to the repo layout.
    """
    if pipeline_dir := os.environ.get("TEKTON_PIPELINE_DIR"):
        return Path(pipeline_dir) / "pipelines" / "python-remediated-build" / "python-remediated-build.yaml"
    # config.py -> python/ -> ecosystems/ -> import_orchestrator/ -> src/ -> project root
    project_root = Path(__file__).resolve().parents[4]
    return project_root / "tekton" / "pipelines" / "python-remediated-build" / "python-remediated-build.yaml"
