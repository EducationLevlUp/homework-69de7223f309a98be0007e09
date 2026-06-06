"""Tests for the config settings module."""

import os
from unittest.mock import patch

from config.settings import (
    get_export_dir,
    get_llm_model,
    get_thread_id,
)


class TestGetLlmModel:
    """Test LLM model configuration."""

    def test_default_model(self):
        """Default model should be openai:gpt-4o."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove LLM_MODEL if set
            os.environ.pop("LLM_MODEL", None)
            result = get_llm_model()
            assert result == "openai:gpt-4o"

    def test_custom_model(self):
        """Custom model should be respected."""
        with patch.dict(os.environ, {"LLM_MODEL": "anthropic:claude-3-opus-20240229"}):
            result = get_llm_model()
            assert result == "anthropic:claude-3-opus-20240229"


class TestGetExportDir:
    """Test export directory configuration."""

    def test_default_export_dir(self):
        """Default export dir should be ./exported_files."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("EXPORT_DIR", None)
            result = get_export_dir()
            assert result.name == "exported_files"

    def test_custom_export_dir(self):
        """Custom export dir should be respected."""
        with patch.dict(os.environ, {"EXPORT_DIR": "/tmp/custom_export"}):
            result = get_export_dir()
            assert str(result) == "/tmp/custom_export"


class TestGetThreadId:
    """Test thread ID configuration."""

    def test_custom_thread_id(self):
        """Custom thread ID should be respected."""
        with patch.dict(os.environ, {"THREAD_ID": "my-custom-thread"}):
            result = get_thread_id()
            assert result == "my-custom-thread"

    def test_auto_generated_thread_id(self):
        """Auto-generated thread ID should be a valid UUID string."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("THREAD_ID", None)
            result = get_thread_id()
            # Should be a non-empty string (UUID)
            assert isinstance(result, str)
            assert len(result) > 0
