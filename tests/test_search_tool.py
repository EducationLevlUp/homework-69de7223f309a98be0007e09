"""Tests for the search tool module."""

from unittest.mock import MagicMock, patch


class TestCreateSearchTool:
    """Test search tool creation."""

    def test_create_search_tool_returns_instance(self):
        """create_search_tool should return a DuckDuckGoSearchResults instance."""
        mock_instance = MagicMock()
        mock_instance.name = "internet_search"
        mock_instance.description = "Search the internet for current information."

        # Patch at the point of use inside tools.search, not the external package
        with patch(
            "tools.search.DuckDuckGoSearchResults",
            return_value=mock_instance,
        ) as mock_ddg:
            from tools.search import create_search_tool

            tool = create_search_tool()
            assert tool is not None
            assert tool.name == "internet_search"
            assert tool.description is not None
            assert "search" in tool.description.lower() or "internet" in tool.description.lower()
            mock_ddg.assert_called_once()

    def test_search_tool_has_invoke_method(self):
        """Search tool should have an invoke method."""
        mock_instance = MagicMock()
        mock_instance.invoke = MagicMock()

        with patch(
            "tools.search.DuckDuckGoSearchResults",
            return_value=mock_instance,
        ):
            from tools.search import create_search_tool

            tool = create_search_tool()
            assert hasattr(tool, "invoke") or hasattr(tool, "_run")

    def test_search_tool_name(self):
        """Search tool should have the correct name."""
        mock_instance = MagicMock()
        mock_instance.name = "internet_search"

        with patch(
            "tools.search.DuckDuckGoSearchResults",
            return_value=mock_instance,
        ):
            from tools.search import create_search_tool

            tool = create_search_tool()
            assert tool.name == "internet_search"
