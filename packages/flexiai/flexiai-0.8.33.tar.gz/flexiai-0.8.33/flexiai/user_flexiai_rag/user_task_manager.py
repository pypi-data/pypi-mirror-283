# user_flexiai_rag/user_task_manager.py
import logging
import subprocess
import urllib.parse
import pandas as pd
from flexiai.config.logging_config import setup_logging
from flexiai.user_flexiai_rag.user_helpers import format_product

# Set up logging using your custom configuration
setup_logging()


class UserTaskManager:
    """
    UserTaskManager class handles user-defined tasks.
    """

    def __init__(self):
        """
        Initializes the UserTaskManager instance, setting up the logger.
        """
        self.logger = logging.getLogger(__name__)


    def search_youtube(self, query):
        """
        Searches YouTube for the given query and opens the search results page
        in the default web browser.

        Args:
            query (str): The search query string.

        Returns:
            dict: A dictionary containing the status, message, and result (URL)
        """
        if not query:
            return {
                "status": False,
                "message": "Query cannot be empty.",
                "result": None
            }

        try:
            # Normalize spaces to ensure consistent encoding
            query_normalized = query.replace(" ", "+")
            query_encoded = urllib.parse.quote(query_normalized)
            youtube_search_url = (
                f"https://www.youtube.com/results?search_query={query_encoded}"
            )
            self.logger.info(f"Opening YouTube search for query: {query}")

            # subprocess.run(['cmd.exe', '/c', 'start', '', youtube_search_url], check=True)

            # Use PowerShell to open the URL
            subprocess.run(
                ['powershell.exe', '-Command', 'Start-Process', youtube_search_url],
                check=True
            )

            self.logger.info("YouTube search page opened successfully.")
            return {
                "status": True,
                "message": "YouTube search page opened successfully.",
                "result": youtube_search_url
            }
        except subprocess.CalledProcessError as e:
            error_message = f"Subprocess error: {str(e)}"
            self.logger.error(error_message, exc_info=True)
            return {
                "status": False,
                "message": error_message,
                "result": None
            }
        except Exception as e:
            error_message = f"Failed to open YouTube search for query: {query}. Error: {str(e)}"
            self.logger.error(error_message, exc_info=True)
            return {
                "status": False,
                "message": error_message,
                "result": None
            }


    def search_products(self, product_id=None, product_name=None, brand=None, price_range=None, stock=None, rating_range=None, 
                        warranty_years=None, category=None, release_date=None, customer_reviews=None):
        """
        Searches for products in the products CSV file based on the given criteria.

        Args:
            product_id (int, optional): The ID of the product.
            product_name (str, optional): The name of the product.
            brand (str or list, optional): The brand of the product or a list of brands.
            price_range (tuple, optional): The price range as a tuple (min_price, max_price).
            stock (int, optional): The stock quantity.
            rating_range (tuple, optional): The rating range as a tuple (min_rating, max_rating).
            warranty_years (int, optional): The number of warranty years.
            category (str, optional): The category of the product.
            release_date (str, optional): The release date of the product.
            customer_reviews (str, optional): A substring to search for in customer reviews.

        Returns:
            dict: A dictionary containing the status, message, and result (formatted product list or None).
        """
        try:
            # Load the CSV file
            df = pd.read_csv('flexiai/user_flexiai_rag/data/products.csv')

            # Apply filters based on the provided arguments
            if product_id is not None:
                df = df[df['product_id'] == product_id]
            if product_name is not None:
                df = df[df['product_name'].str.contains(product_name, case=False, na=False)]
            if brand is not None:
                if isinstance(brand, list):
                    df = df[df['brand'].isin(brand)]
                else:
                    df = df[df['brand'].str.contains(brand, case=False, na=False)]
            if price_range is not None:
                if isinstance(price_range, tuple) and len(price_range) == 2:
                    df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]
                else:
                    error_message = "Invalid price range. Provide a tuple with (min_price, max_price)."
                    self.logger.error(error_message)
                    return {
                        "status": False,
                        "message": error_message,
                        "result": None
                    }
            if stock is not None:
                df = df[df['stock'] == stock]
            if rating_range is not None:
                if isinstance(rating_range, tuple) and len(rating_range) == 2:
                    df = df[(df['rating'] >= rating_range[0]) & (df['rating'] <= rating_range[1])]
                else:
                    error_message = "Invalid rating range. Provide a tuple with (min_rating, max_rating)."
                    self.logger.error(error_message)
                    return {
                        "status": False,
                        "message": error_message,
                        "result": None
                    }
            if warranty_years is not None:
                df = df[df['warranty_years'] == warranty_years]
            if category is not None:
                df = df[df['category'].str.contains(category, case=False, na=False)]
            if release_date is not None:
                df = df[df['release_date'] == release_date]
            if customer_reviews is not None:
                df = df[df['customer_reviews'].str.contains(customer_reviews, case=False, na=False)]

            # Check if any results are found
            if df.empty:
                return {
                    "status": False,
                    "message": "No products found matching the criteria.",
                    "result": None
                }

            # Convert the filtered DataFrame to a list of dictionaries
            results = df.to_dict(orient='records')
            # Format each product using the format_product function
            formatted_results = [format_product(product) for product in results]
            return {
                "status": True,
                "message": f"Found {len(formatted_results)} product(s) matching the criteria.",
                "result": formatted_results
            }
        except FileNotFoundError:
            error_message = "The products.csv file was not found."
            self.logger.error(error_message, exc_info=True)
            return {
                "status": False,
                "message": error_message,
                "result": None
            }
        except pd.errors.EmptyDataError:
            error_message = "The products.csv file is empty."
            self.logger.error(error_message, exc_info=True)
            return {
                "status": False,
                "message": error_message,
                "result": None
            }
        except Exception as e:
            error_message = f"An error occurred while searching for products: {str(e)}"
            self.logger.error(error_message, exc_info=True)
            return {
                "status": False,
                "message": error_message,
                "result": None
            }

    # User can add more custom tasks (assistant personal functions or functions to call other assistants)
