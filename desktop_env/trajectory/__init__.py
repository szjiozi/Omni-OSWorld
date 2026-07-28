"""Versioned trajectory recording for OSWorld episodes."""

from desktop_env.trajectory.recorder import TrajectoryRecorder
from desktop_env.trajectory.schema import SCHEMA_VERSION, validate_document

__all__ = ["SCHEMA_VERSION", "TrajectoryRecorder", "validate_document"]
