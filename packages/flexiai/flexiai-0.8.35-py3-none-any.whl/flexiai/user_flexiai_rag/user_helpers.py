# user_flexiai_rag/user_helpers.py
import subprocess
import logging

def wsl_to_windows_path(wsl_path):
    """
    Converts a WSL path to a Windows path.

    Args:
        wsl_path (str): The WSL path to convert.

    Returns:
        str: The converted Windows path, or None if an error occurs.
    """
    try:
        windows_path = subprocess.check_output(['wslpath', '-w', wsl_path]).strip().decode('utf-8')
        return windows_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting WSL path to Windows path: {e}")
        return None

def format_product(product):
    """
    Formats product details into a readable string.

    Args:
        product (dict): A dictionary containing product details. Expected keys are 'product_id', 
                        'product_name', 'brand', 'price', 'stock', 'rating', 'warranty_years', 
                        'category', 'release_date', and 'customer_reviews'.

    Returns:
        str: A formatted string containing the product details.
    """
    return (
        f"Product ID: {product['product_id']}\n"
        f"Product Name: {product['product_name']}\n"
        f"Brand: {product['brand']}\n"
        f"Price: ${product['price']}\n"
        f"Stock: {product['stock']}\n"
        f"Rating: {product['rating']}\n"
        f"Warranty Years: {product['warranty_years']}\n"
        f"Category: {product['category']}\n"
        f"Release Date: {product['release_date']}\n"
        f"Customer Reviews: {product['customer_reviews']}\n\n"
    )
