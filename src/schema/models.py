from enum import StrEnum, auto
from typing import TypeAlias

# TODO: move to the local module
class WorkflowEnum(StrEnum):
    proportion_agent = "proportion_agent"
    associations_insights = "associations_insights"
    standout_insights = "standout_insights"
    dev_workflow = "dev_workflow"
    e2e_workflow = "e2e_workflow"
