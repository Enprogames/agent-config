"""Copy or download validated image assets into an isolated render directory."""

from __future__ import annotations

import mimetypes
import shutil
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlparse

from scripts.markdown_qa.errors import MarkdownQaError

MAX_REMOTE_IMAGE_BYTES = 25 * 1024 * 1024


def _file_uri_path(source: str) -> Path:
    parsed = urlparse(source)
    value = unquote(parsed.path)
    if len(value) >= 3 and value[0] == "/" and value[2] == ":":
        value = value[1:]
    return Path(value)


class AssetResolver:
    """Stage image assets and keep browser rendering deterministic."""

    def __init__(
        self,
        source_dir: Path,
        staging_dir: Path,
        *,
        allow_remote: bool,
    ) -> None:
        self.source_dir = source_dir
        self.media_dir = staging_dir / "media"
        self.media_dir.mkdir(parents=True, exist_ok=True)
        self.allow_remote = allow_remote
        self.local_count = 0
        self.remote_count = 0
        self._counter = 0

    def _destination(self, suffix: str) -> Path:
        self._counter += 1
        safe_suffix = suffix.casefold() if suffix else ".img"
        return self.media_dir / f"asset-{self._counter:03d}{safe_suffix}"

    def resolve(self, source: str) -> str:
        if source.startswith("data:"):
            return source
        parsed = urlparse(source)
        if parsed.scheme in {"http", "https"}:
            if not self.allow_remote:
                raise MarkdownQaError(
                    "Remote image rendering is disabled; authorize network access and "
                    "pass --allow-remote-assets when it is required."
                )
            self.remote_count += 1
            return self._download(source)
        if parsed.scheme == "file":
            candidate = _file_uri_path(source)
        else:
            local_source = source.split("#", maxsplit=1)[0]
            local_source = local_source.split("?", maxsplit=1)[0]
            candidate = Path(unquote(local_source))
            if not candidate.is_absolute():
                candidate = self.source_dir / candidate
        if not candidate.is_file():
            raise MarkdownQaError(f"Referenced image does not exist: {source}")
        destination = self._destination(candidate.suffix)
        shutil.copy2(candidate, destination)
        self.local_count += 1
        return destination.relative_to(self.media_dir.parent).as_posix()

    def _download(self, source: str) -> str:
        request = urllib.request.Request(
            source, headers={"User-Agent": "technical-document-markdown-qa/0.1"}
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                content_type = response.headers.get_content_type()
                data = response.read(MAX_REMOTE_IMAGE_BYTES + 1)
        except OSError as exc:
            raise MarkdownQaError(
                f"Could not download remote image {source}: {exc}"
            ) from exc
        if len(data) > MAX_REMOTE_IMAGE_BYTES:
            raise MarkdownQaError(f"Remote image exceeds 25 MiB: {source}")
        if not content_type.startswith("image/"):
            raise MarkdownQaError(
                f"Remote asset is not an image ({content_type}): {source}"
            )
        parsed = urlparse(source)
        suffix = (
            mimetypes.guess_extension(content_type)
            or Path(parsed.path).suffix
            or ".img"
        )
        destination = self._destination(suffix)
        destination.write_bytes(data)
        return destination.relative_to(self.media_dir.parent).as_posix()
