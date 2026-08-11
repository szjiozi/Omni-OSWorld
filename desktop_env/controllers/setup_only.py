"""Minimal setup controller for evaluator-free human annotation tasks."""

from __future__ import annotations

import logging
import os
from typing import Any

import requests


logger = logging.getLogger("desktopenv.setup_only")


class SetupOnlyController:
    """Support only trusted local upload and open actions."""

    ALLOWED_TYPES = {"upload_file", "open"}

    def __init__(
        self,
        vm_ip: str,
        server_port: int = 5000,
        chromium_port: int = 9222,
        vlc_port: int = 8080,
        cache_dir: str = "cache",
        client_password: str = "",
        screen_width: int = 1920,
        screen_height: int = 1080,
    ) -> None:
        del chromium_port, vlc_port, client_password, screen_width, screen_height
        self.http_server = f"http://{vm_ip}:{server_port}"
        self.cache_dir = cache_dir

    def reset_cache_dir(self, cache_dir: str) -> None:
        self.cache_dir = cache_dir

    def setup(self, config: list[dict[str, Any]], use_proxy: bool = False) -> bool:
        if use_proxy:
            raise ValueError("SetupOnlyController does not support proxy setup")
        for index, step in enumerate(config, start=1):
            action_type = step.get("type")
            if action_type not in self.ALLOWED_TYPES:
                raise ValueError(
                    f"Unsupported setup-only action at index {index}: "
                    f"{action_type!r}"
                )
            parameters = step.get("parameters", {})
            if action_type == "upload_file":
                self._upload_files(parameters.get("files", []))
            else:
                self._open(parameters.get("path", ""))
        return True

    def _upload_files(self, files: list[dict[str, str]]) -> None:
        if not files:
            raise ValueError("upload_file requires at least one file")
        for file_config in files:
            local_path = file_config.get("local_path", "")
            guest_path = file_config.get("path", "")
            if not local_path or not os.path.isfile(local_path):
                raise FileNotFoundError(
                    f"Setup upload source does not exist: {local_path}"
                )
            if not guest_path:
                raise ValueError("Setup upload destination must not be empty")
            with open(local_path, "rb") as stream:
                response = requests.post(
                    f"{self.http_server}/setup/upload",
                    data={"file_path": guest_path},
                    files={
                        "file_data": (
                            os.path.basename(guest_path),
                            stream,
                            "application/octet-stream",
                        )
                    },
                    timeout=(10, 600),
                )
            response.raise_for_status()
            logger.info("Uploaded %s to %s", local_path, guest_path)

    def _open(self, path: str) -> None:
        if not path:
            raise ValueError("open requires a guest path")
        response = requests.post(
            f"{self.http_server}/setup/open_file",
            json={"path": path},
            timeout=1810,
        )
        response.raise_for_status()
        logger.info("Opened guest artifact %s", path)
