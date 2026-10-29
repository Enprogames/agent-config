"""Capture the preceding stored Codex final answer without model rewriting."""

from __future__ import annotations

import hashlib
import json
import os
import queue
import shutil
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

from scripts.response_pdf.errors import CaptureError


def _codex_command() -> list[str]:
    explicit = os.environ.get("RESPONSE_PDF_CODEX_BIN")
    if explicit:
        if Path(explicit).suffix.casefold() in {".bat", ".cmd"}:
            return _windows_wrapper_command(explicit)
        return [explicit, "app-server", "--listen", "stdio://"]

    wrapper = shutil.which("codex.cmd") if os.name == "nt" else None
    if wrapper:
        return _windows_wrapper_command(wrapper)
    executable = shutil.which("codex.exe") or shutil.which("codex")
    if executable:
        return [executable, "app-server", "--listen", "stdio://"]
    raise CaptureError(
        "Codex App Server was not found. Supply Markdown explicitly or set "
        "RESPONSE_PDF_CODEX_BIN."
    )


def _windows_wrapper_command(wrapper: str) -> list[str]:
    wrapper_path = Path(wrapper).resolve()
    node = wrapper_path.with_name("node.exe")
    codex_script = (
        wrapper_path.parent / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
    )
    if node.is_file() and codex_script.is_file():
        return [
            str(node),
            str(codex_script),
            "app-server",
            "--listen",
            "stdio://",
        ]
    comspec = os.environ.get("COMSPEC", "cmd.exe")
    invocation = f'"{wrapper}" app-server --listen stdio://'
    return [comspec, "/d", "/s", "/c", invocation]


def _reader(stream: Any, messages: queue.Queue[dict[str, Any]]) -> None:
    for line in stream:
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            messages.put(value)


def _wait_for_id(
    messages: queue.Queue[dict[str, Any]], request_id: int, timeout: float
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            message = messages.get(timeout=min(0.25, deadline - time.monotonic()))
        except queue.Empty:
            continue
        if message.get("id") == request_id:
            return message
    raise CaptureError(f"Codex App Server timed out waiting for request {request_id}.")


def _send(stream: Any, message: dict[str, Any]) -> None:
    stream.write(json.dumps(message, ensure_ascii=False) + "\n")
    stream.flush()


def _read_thread(thread_id: str) -> dict[str, Any]:
    process = subprocess.Popen(
        _codex_command(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if process.stdin is None or process.stdout is None or process.stderr is None:
        process.kill()
        raise CaptureError("Could not open Codex App Server pipes.")

    messages: queue.Queue[dict[str, Any]] = queue.Queue()
    errors: list[str] = []
    threading.Thread(
        target=_reader, args=(process.stdout, messages), daemon=True
    ).start()
    threading.Thread(
        target=lambda: errors.extend(process.stderr.readlines()), daemon=True
    ).start()
    try:
        _send(
            process.stdin,
            {
                "method": "initialize",
                "id": 0,
                "params": {
                    "clientInfo": {
                        "name": "response_to_pdf_skill",
                        "title": "Response to PDF Skill",
                        "version": "0.1.0",
                    }
                },
            },
        )
        initialized = _wait_for_id(messages, 0, 20)
        if "error" in initialized:
            raise CaptureError(f"Codex initialization failed: {initialized['error']}")
        _send(process.stdin, {"method": "initialized", "params": {}})
        _send(
            process.stdin,
            {
                "method": "thread/read",
                "id": 1,
                "params": {"threadId": thread_id, "includeTurns": True},
            },
        )
        response = _wait_for_id(messages, 1, 30)
        if "error" in response:
            raise CaptureError(f"Codex thread read failed: {response['error']}")
        thread = response.get("result", {}).get("thread")
        if not isinstance(thread, dict):
            raise CaptureError("Codex returned no readable thread data.")
        return thread
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        if process.returncode not in {None, 0, 1} and errors:
            errors.clear()


def _last_final_answer(thread: dict[str, Any]) -> str:
    answers: list[str] = []
    turns = thread.get("turns", [])
    for turn in turns if isinstance(turns, list) else []:
        if not isinstance(turn, dict):
            continue
        items = turn.get("items", [])
        for item in items if isinstance(items, list) else []:
            if not isinstance(item, dict) or item.get("type") != "agentMessage":
                continue
            phase = item.get("phase")
            text = item.get("text")
            if phase in {None, "final_answer"} and isinstance(text, str) and text:
                answers.append(text)
    if not answers:
        raise CaptureError(
            "No preceding completed Codex final answer was found in the stored thread."
        )
    return answers[-1]


def capture_last_codex_answer(output: Path) -> dict[str, Any]:
    """Write the exact stored preceding Codex final answer as UTF-8 bytes."""
    thread_id = os.environ.get("CODEX_THREAD_ID") or os.environ.get("CODEX_SESSION_ID")
    if not thread_id:
        raise CaptureError(
            "CODEX_THREAD_ID is unavailable. Exact host capture cannot be claimed."
        )
    text = _last_final_answer(_read_thread(thread_id))
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    encoded = text.encode("utf-8")
    output.write_bytes(encoded)
    return {
        "capture_mode": "codex-app-server",
        "output": str(output),
        "source_bytes": len(encoded),
        "source_sha256": hashlib.sha256(encoded).hexdigest(),
        "thread_id": thread_id,
    }
