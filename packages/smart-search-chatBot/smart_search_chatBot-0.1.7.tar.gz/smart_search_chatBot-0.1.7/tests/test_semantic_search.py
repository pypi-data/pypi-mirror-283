# tests/test_semantic_search.py

import pandas as pd
import pytest
from SMARTSEARCHCHATBOT.semantic_search_chatBot import SemanticSearch

@pytest.fixture
def sample_data():
    data = {
        'product_name': ['apple gift card 100 usd', 'pubg 100 wh', 'amazon 500 ksa'],
        'category_Name_en': ['Gift Cards', 'Games', 'Shopping'],
        'category_id': [1, 2, 3],
        'product_id': [101, 102, 103]
    }
    return pd.DataFrame(data)

@pytest.fixture
def search_instance(sample_data):
    return SemanticSearch(sample_data)

def test_get_product_ids_by_category(search_instance):
    result = search_instance.get_product_ids_by_category(1)
    assert result == {'product_ids': [101]}

def test_semantic_search(search_instance):
    result = search_instance.semantic_search("i want apple gift card 100 usd")
    assert 'product_id' in result
    assert result['product_id'] == 101
