import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from search import find_pages, print_word

# ---- Shared Test Data ----
# Define a sample index here that all tests can reuse
# This avoids repeating the same index in every test

@pytest.fixture
def sample_index():
    """A small sample index for testing search functions"""
    return {
        "good": {
            "http://test.com/1": {"frequency": 2, "positions": [0, 5]},
            "http://test.com/2": {"frequency": 1, "positions": [3]}
        },
        "friends": {
            "http://test.com/2": {"frequency": 1, "positions": [7]},
            "http://test.com/3": {"frequency": 2, "positions": [1, 4]}
        },
        "world": {
            "http://test.com/1": {"frequency": 1, "positions": [2]}
        }
    }


class TestFindPages:

    def test_single_word_found(self, sample_index):
        """Test that a single word query returns correct URLs"""
        query = "world"
        links = find_pages(sample_index, query)
        assert links == ["http://test.com/1"]

    def test_single_word_not_found(self, sample_index):
        """Test that a word not in index returns empty list"""
        query = "nonsense"
        links = find_pages(sample_index, query)
        assert links == []

    def test_multi_word_intersection(self, sample_index):
        """Test that multi-word query returns only pages containing ALL words"""
        query = "good friends"
        links = find_pages(sample_index, query)
        assert links == ["http://test.com/2"]

    def test_multi_word_no_intersection(self, sample_index):
        """Test that multi-word query returns empty list when no page contains all words"""
        query = "world friends"
        links = find_pages(sample_index, query)
        assert links == []

    def test_empty_query(self, sample_index):
        """Test that empty query returns empty list"""
        query = ""
        links = find_pages(sample_index, query)
        assert links == []

    def test_case_insensitive(self, sample_index):
        """Test that search is case insensitive"""
        # "GOOD" should find same results as "good"
        query = "GOOD"
        links = find_pages(sample_index, query)
        assert set(links) == {"http://test.com/1", "http://test.com/2"}

    def test_multi_word_single_result(self, sample_index):
        """Test multi-word query that resolves to a single page"""
        # "good" and "world" are both on page 1 only
        query = "good world"
        links = find_pages(sample_index, query)
        assert links == ["http://test.com/1"]


class TestPrintWord:

    def test_word_found(self, sample_index, capsys):
        """Test that print_word outputs correct information"""
        # capsys captures printed output so you can assert on it
        print_word(sample_index, "good")
        captured = capsys.readouterr()
        assert "good" in captured.out

    def test_word_not_found(self, sample_index, capsys):
        """Test that print_word handles missing word gracefully"""
        print_word(sample_index, "nonsense")
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_case_insensitive(self, sample_index, capsys):
        """Test that print_word is case insensitive"""
        # "GOOD" should find same result as "good"
        print_word(sample_index, "GOOD")
        captured = capsys.readouterr()
        assert "good" in captured.out