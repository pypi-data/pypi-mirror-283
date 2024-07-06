# tests/test_assistant_search_product.py
import pytest
from flexiai.user_flexiai_rag.user_task_manager import UserTaskManager

@pytest.fixture
def task_manager():
    return UserTaskManager()

def test_search_by_product_id(task_manager):
    result = task_manager.search_products(product_id=101)
    print("test_search_by_product_id result:", result)
    assert result['status'] == True
    assert len(result['result']) == 1
    assert 'Product Name: Laptop' in result['result'][0]

def test_search_by_product_name(task_manager):
    result = task_manager.search_products(product_name='Smartphone')
    print("test_search_by_product_name result:", result)
    assert result['status'] == True
    assert len(result['result']) == 1
    assert 'Product Name: Smartphone' in result['result'][0]

def test_search_by_brand(task_manager):
    result = task_manager.search_products(brand='BrandC')
    print("test_search_by_brand result:", result)
    assert result['status'] == True
    assert len(result['result']) == 2
    assert 'Product Name: Tablet' in result['result'][0]

def test_search_by_price_range(task_manager):
    result = task_manager.search_products(price_range=(100, 400))
    print("test_search_by_price_range result:", result)
    assert result['status'] == True
    assert len(result['result']) == 9

def test_search_by_rating_range(task_manager):
    result = task_manager.search_products(rating_range=(4.0, 4.5))
    print("test_search_by_rating_range result:", result)
    assert result['status'] == True
    assert len(result['result']) == 24

def test_search_by_multiple_criteria(task_manager):
    result = task_manager.search_products(brand='BrandD', price_range=(100, 300))
    print("test_search_by_multiple_criteria result:", result)
    assert result['status'] == True
    assert len(result['result']) == 2
    assert 'Product Name: Smartwatch' in result['result'][0]

def test_search_by_multiple_brands(task_manager):
    result = task_manager.search_products(brand=['BrandC', 'BrandD'])
    print("test_search_by_multiple_brands result:", result)
    assert result['status'] == True
    assert len(result['result']) == 2

def test_no_results_found(task_manager):
    result = task_manager.search_products(product_name='NonExistentProduct')
    print("test_no_results_found result:", result)
    assert result['status'] == False
    assert result['result'] is None

def test_invalid_price_range(task_manager):
    result = task_manager.search_products(price_range=(100,))
    print("test_invalid_price_range result:", result)
    assert result['status'] == False
    assert result['result'] is None
    assert result['message'] == "Invalid price range. Provide a tuple with (min_price, max_price)."

def test_invalid_rating_range(task_manager):
    result = task_manager.search_products(rating_range=(4.0,))
    print("test_invalid_rating_range result:", result)
    assert result['status'] == False
    assert result['result'] is None
    assert result['message'] == "Invalid rating range. Provide a tuple with (min_rating, max_rating)."
