"""Tests for the export hook module."""

from pathlib import Path

import pytest

from agent.export_hook import _resolve_safe_path, export_virtual_files


class TestResolveSafePath:
    """Test safe path resolution to prevent directory traversal."""

    def test_normal_path(self, tmp_path: Path):
        """Normal relative path should resolve correctly."""
        result = _resolve_safe_path(tmp_path, "subdir/file.txt")
        assert result == tmp_path / "subdir" / "file.txt"

    def test_root_path(self, tmp_path: Path):
        """Root-level file should resolve correctly."""
        result = _resolve_safe_path(tmp_path, "file.txt")
        assert result == tmp_path / "file.txt"

    def test_directory_traversal_blocked(self, tmp_path: Path):
        """Path traversal attempts should be blocked."""
        with pytest.raises(ValueError, match="escape"):
            _resolve_safe_path(tmp_path, "../etc/passwd")

    def test_nested_traversal_blocked(self, tmp_path: Path):
        """Nested traversal should also be blocked."""
        with pytest.raises(ValueError, match="escape"):
            _resolve_safe_path(tmp_path, "subdir/../../etc/passwd")


class TestExportVirtualFiles:
    """Test virtual file export functionality."""

    def test_export_from_files_key(self, tmp_path: Path):
        """Export files stored under 'files' key in state."""
        state = {
            "files": {
                "report.txt": "Research findings here",
                "summary.md": "# Summary\n\nKey points:",
            }
        }

        exported = export_virtual_files(state, tmp_path)

        assert len(exported) == 2
        assert (tmp_path / "report.txt").read_text() == "Research findings here"
        assert (tmp_path / "summary.md").read_text() == "# Summary\n\nKey points:"

    def test_export_from_virtual_files_key(self, tmp_path: Path):
        """Export files stored under 'virtual_files' key in state."""
        state = {
            "virtual_files": {
                "data/results.json": '{"key": "value"}',
            }
        }

        exported = export_virtual_files(state, tmp_path)

        assert len(exported) == 1
        assert (tmp_path / "data" / "results.json").read_text() == '{"key": "value"}'

    def test_export_creates_directory(self, tmp_path: Path):
        """Export should create nested directories as needed."""
        state = {
            "files": {
                "deep/nested/path/file.txt": "content",
            }
        }

        exported = export_virtual_files(state, tmp_path)

        assert len(exported) == 1
        assert (tmp_path / "deep" / "nested" / "path" / "file.txt").exists()

    def test_export_empty_state(self, tmp_path: Path):
        """Export with no virtual files should return empty list."""
        state = {"messages": []}

        exported = export_virtual_files(state, tmp_path)

        assert exported == []

    def test_export_preserves_content(self, tmp_path: Path):
        """Export should preserve file content exactly."""
        content = "Line 1\nLine 2\nLine 3"
        state = {"files": {"test.txt": content}}

        export_virtual_files(state, tmp_path)

        assert (tmp_path / "test.txt").read_text() == content

    def test_export_with_default_dir(self):
        """Export should use default directory when not specified."""
        state = {"files": {"test.txt": "content"}}

        exported = export_virtual_files(state)

        assert len(exported) == 1
        assert exported[0].exists()
        # Clean up
        exported[0].unlink()
        if exported[0].parent.exists() and exported[0].parent.name == "exported_files":
            exported[0].parent.rmdir()
