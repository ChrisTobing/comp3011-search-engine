import json
import sys
import os
from unittest import result
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from indexer import build_index, save_index, load_index

class TestBuildIndex:

    def test_basic_frequency(self):
        """Test that word frequency is counted correctly"""
        pages = [{"url": "http://test.com", "content": "good good bad"}]
        index = build_index(pages)
        assert index["good"]["http://test.com"]["frequency"] == 2

    def test_basic_positions(self):
        """Test that word positions are recorded correctly"""
        pages = [{"url": "http://test.com", "content": "good bad good"}]
        index = build_index(pages)
        assert index["good"]["http://test.com"]["positions"] == [0, 2]

    def test_case_insensitive(self):
        """Test that Good and good are treated as the same word"""
        pages = [{"url": "http://test.com", "content": "Good good GOOD"}]
        index = build_index(pages)
        assert index["good"]["http://test.com"]["frequency"] == 3

    def test_empty_pages(self):
        """Test that empty pages list returns empty index"""
        index = build_index([])
        assert index == {}

    def test_multiple_pages(self):
        """Test that words are indexed across multiple pages"""
        pages = [
            {"url": "http://test.com/1", "content": "good world"},
            {"url": "http://test.com/2", "content": "good friends"}
        ]
        index = build_index(pages)
        assert "http://test.com/1" in index["good"]
        assert "http://test.com/2" in index["good"]

class TestSaveLoadIndex:
    def test_save_load_consistency(self, tmp_path):
        """Test that saving and loading the index preserves its structure"""
        filepath = tmp_path / "test_index.json"
        index = {
            "good": {
                "http://test.com": {"frequency": 2, "positions": [0, 2]}
            }
        }
        save_index(index, filepath=filepath)
        loaded_index = load_index(filepath=filepath)
        assert loaded_index == index
    
    def test_save_empty_index(self, tmp_path):
        """Test that saving and loading an empty index works correctly"""
        filepath = tmp_path / "test_empty_index.json"
        index = {}
        save_index(index, filepath=filepath)
        loaded_index = load_index(filepath=filepath)
        assert loaded_index == index
    
    def test_save_index_overwrite(self, tmp_path):
        """Test that saving an index overwrites existing file"""
        filepath = tmp_path / "test_overwrite.json"
        index1 = {"word": {"http://test.com": {"frequency": 1, "positions": [0]}}}
        index2 = {"word": {"http://test.com": {"frequency": 2, "positions": [0, 1]}}}
        save_index(index1, filepath=filepath)
        save_index(index2, filepath=filepath)
        loaded_index = load_index(filepath=filepath)
        assert loaded_index == index2
    
    def test_save_index_invalid_path(self):
        """Test that saving to an invalid path raises an error"""
        index = {"word": {"http://test.com": {"frequency": 1, "positions": [0]}}}
        with pytest.raises(FileNotFoundError):
            save_index(index, filepath="/invalid_path/test.json")
        
    def test_load_index_invalid_json(self):
        """Test that loading an invalid JSON file raises an error"""
        with open("invalid.json", "w") as f:
            f.write("This is not valid JSON")
        with pytest.raises(json.JSONDecodeError):
            load_index(filepath="invalid.json")

    def test_load_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            load_index(filepath="nonexistent.json")