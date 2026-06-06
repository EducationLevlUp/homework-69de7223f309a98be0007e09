"""Export hook module: syncs virtual files from StateBackend to real filesystem."""

from pathlib import Path

from config.settings import get_export_dir


def export_virtual_files(state: dict, export_dir: Path | None = None) -> list[Path]:
    """Export virtual files from agent state to the real filesystem.

    Args:
        state: The final agent state containing virtual file data.
        export_dir: Target directory for exported files. Defaults to config setting.

    Returns:
        List of paths to exported files.
    """
    if export_dir is None:
        export_dir = get_export_dir()

    # Create export directory if it doesn't exist
    export_dir.mkdir(parents=True, exist_ok=True)

    exported_files: list[Path] = []

    # Extract virtual files from state
    # StateBackend stores files under a 'files' or 'virtual_files' key
    virtual_files = _extract_virtual_files(state)

    for file_path, content in virtual_files.items():
        # Resolve the target path safely (prevent directory traversal)
        target_path = _resolve_safe_path(export_dir, file_path)

        # Write content to real filesystem
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")
        exported_files.append(target_path)

    return exported_files


def _extract_virtual_files(state: dict) -> dict[str, str]:
    """Extract virtual file contents from agent state.

    The StateBackend stores files in the state under various possible keys.
    We check common patterns used by deepagents.

    Args:
        state: Agent state dictionary.

    Returns:
        Dictionary mapping file paths to their contents.
    """
    virtual_files: dict[str, str] = {}

    # Try common state keys where StateBackend might store files
    possible_keys = ["files", "virtual_files", "backend_files", "file_store"]

    for key in possible_keys:
        if key in state and isinstance(state[key], dict):
            for path, content in state[key].items():
                if isinstance(content, str):
                    virtual_files[path] = content
            if virtual_files:
                return virtual_files

    # If no dedicated key found, check for file-related entries in state
    for _key, value in state.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, str) and (
                    sub_key.endswith((".txt", ".md", ".json", ".csv", ".py"))
                    or "/" in sub_key
                ):
                    virtual_files[sub_key] = sub_value

    return virtual_files


def _resolve_safe_path(base_dir: Path, relative_path: str) -> Path:
    """Resolve a file path safely, preventing directory traversal attacks.

    Args:
        base_dir: The base directory for exports.
        relative_path: The relative file path from virtual filesystem.

    Returns:
        Resolved absolute path within base_dir.

    Raises:
        ValueError: If the resolved path escapes the base directory.
    """
    # Normalize the path
    target = (base_dir / relative_path).resolve()
    base_resolved = base_dir.resolve()

    # Ensure the target is within the base directory
    try:
        target.relative_to(base_resolved)
    except ValueError as exc:
        raise ValueError(
            f"File path '{relative_path}' would escape the export directory. "
            f"Blocked for security."
        ) from exc

    return target
