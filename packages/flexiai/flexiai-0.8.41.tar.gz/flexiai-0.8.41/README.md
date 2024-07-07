# FlexiAI

FlexiAI is a versatile and powerful AI framework designed to simplify the use of OpenAI and Azure OpenAI APIs. By leveraging advanced Retrieval-Augmented Generation (RAG) capabilities, FlexiAI enables developers to build sophisticated, custom AI assistants efficiently and effectively.

![FlexiAI Framework](assets/flexiai_framework_01.png)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Multi-Platform Integration**: Supports both OpenAI and Azure OpenAI services, offering flexibility and broad compatibility.
- **Configurable and Extensible**: Easily configurable and highly extensible to meet specific project requirements.
- **Robust Logging**: Comprehensive logging for effective debugging and monitoring.
- **Task Management**: Efficiently manages and executes a wide range of tasks.
- **Retrieval-Augmented Generation (RAG)**: Enables AI assistants to dynamically call external functions or services for real-time information retrieval and complex operations.
- **Examples and Tests**: Includes example scripts and comprehensive tests for quick onboarding and reliable performance.
- **Secure and Scalable**: Suitable for both small projects and large enterprise applications.
- **Community-Driven**: Actively maintained and supported by a community of developers.

## Installation

### Create a Virtual Environment

#### Using PowerShell

```powershell
python -m venv env
source env/bin/activate
```

#### Using Conda

```bash
conda create --name flexiai_env python=3.10
conda activate flexiai_env
```

### Install FlexiAI with `pip`

To install the FlexiAI framework using `pip`, run:

```bash
pip install flexiai
```

### Post-Installation Setup

After installing, copy the `post_install.py` file to your project root directory and run it manually to set up additional necessary directories and files.

```bash
python post_install.py
```

#### Or create a new file `post_install.py` in the root directory of your project.

---


<details>
    <summary>⚠️ Attention! Click to expand and copy the code for `post_install.py` ⚠️</summary>

    import os
    
    def create_logs_folder(project_root):
        log_folder = os.path.join(project_root, 'logs')
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
            print(f"Created directory: {log_folder}")
    
    def create_user_flexiai_rag_folder(project_root):
        dst_folder = os.path.join(project_root, 'user_flexiai_rag')
        data_folder = os.path.join(dst_folder, 'data')
        
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
            print(f"Created directory: {data_folder}")
        
        files_content = {
            '__init__.py': "# user_flexiai_rag/__init__.py\n",
            'user_function_mapping.py': (
                "# user_flexiai_rag/user_function_mapping.py\n"
                "from user_flexiai_rag.user_task_manager import UserTaskManager\n\n"
                "def register_user_tasks():\n"
                "    \"\"\"\n"
                "    Register user-defined tasks with the FlexiAI framework.\n\n"
                "    Returns:\n"
                "        tuple: A tuple containing the personal function mappings and assistant\n"
                "        function mappings.\n"
                "    \"\"\"\n"
                "    # Initialize UserTaskManager to access user-defined tasks\n"
                "    task_manager = UserTaskManager()\n\n"
                "    personal_function_mapping = {\n"
                "        'search_youtube': task_manager.search_youtube,\n"
                "        'search_products': task_manager.search_products,\n"
                "        # Add other personal functions here\n"
                "        # 'my_custom_task': task_manager.my_custom_task\n"
                "    }\n\n"
                "    assistant_function_mapping = {\n"
                "        # Add other functions that call assistants here -> the functions must end with \"_assistant\"\n"
                "        # 'call_example_assistant': task_manager.call_example_assistant,\n"
                "    }\n\n"
                "    return personal_function_mapping, assistant_function_mapping\n"
            ),
            'user_helpers.py': (
                "# user_flexiai_rag/user_helpers.py\n"
                "def format_product(product):\n"
                "    \"\"\"\n"
                "    Formats product details into a readable string.\n\n"
                "    Args:\n"
                "        product (dict): A dictionary containing product details. Expected keys are 'product_id', \n"
                "                        'product_name', 'brand', 'price', 'stock', 'rating', 'warranty_years', \n"
                "                        'category', 'release_date', and 'customer_reviews'.\n\n"
                "    Returns:\n"
                "        str: A formatted string containing the product details.\n"
                "    \"\"\"\n"
                "    return (\n"
                "        f\"Product ID: {product['product_id']}\\n\"\n"
                "        f\"Product Name: {product['product_name']}\\n\"\n"
                "        f\"Brand: {product['brand']}\\n\"\n"
                "        f\"Price: ${product['price']}\\n\"\n"
                "        f\"Stock: {product['stock']}\\n\"\n"
                "        f\"Rating: {product['rating']}\\n\"\n"
                "        f\"Warranty Years: {product['warranty_years']}\\n\"\n"
                "        f\"Category: {product['category']}\\n\"\n"
                "        f\"Release Date: {product['release_date']}\\n\"\n"
                "        f\"Customer Reviews: {product['customer_reviews']}\\n\\n\"\n"
                "    )\n"
            ),
            'user_task_manager.py': (
                "# user_flexiai_rag/user_task_manager.py\n"
                "import logging\n"
                "import subprocess\n"
                "import urllib.parse\n"
                "import pandas as pd\n"
                "from flexiai.config.logging_config import setup_logging\n"
                "from user_flexiai_rag.user_helpers import format_product\n\n"
                "# Set up logging using your custom configuration\n"
                "# Adjust the logging levels as per your requirements\n"
                "setup_logging(root_level=logging.INFO, file_level=logging.DEBUG, console_level=logging.ERROR)\n\n\n"
                "class UserTaskManager:\n"
                "    \"\"\"\n"
                "    UserTaskManager class handles user-defined tasks.\n"
                "    \"\"\"\n\n"
                "    def __init__(self):\n"
                "        \"\"\"\n"
                "        Initializes the UserTaskManager instance, setting up the logger.\n"
                "        \"\"\"\n"
                "        self.logger = logging.getLogger(__name__)\n\n\n"
                "    def search_youtube(self, query):\n"
                "        \"\"\"\n"
                "        Searches YouTube for the given query and opens the search results page\n"
                "        in the default web browser.\n\n"
                "        Args:\n"
                "            query (str): The search query string.\n\n"
                "        Returns:\n"
                "            dict: A dictionary containing the status, message, and result (URL)\n"
                "        \"\"\"\n"
                "        if not query:\n"
                "            return {\n"
                "                \"status\": False,\n"
                "                \"message\": \"Query cannot be empty.\",\n"
                "                \"result\": None\n"
                "            }\n\n"
                "        try:\n"
                "            # Normalize spaces to ensure consistent encoding\n"
                "            query_normalized = query.replace(\" \", \"+\")\n"
                "            query_encoded = urllib.parse.quote(query_normalized)\n"
                "            youtube_search_url = (\n"
                "                f\"https://www.youtube.com/results?search_query={query_encoded}\"\n"
                "            )\n"
                "            self.logger.info(f\"Opening YouTube search for query: {query}\")\n\n"
                "            # subprocess.run(['cmd.exe', '/c', 'start', '', youtube_search_url], check=True)\n\n"
                "            # Use PowerShell to open the URL\n"
                "            subprocess.run(\n"
                "                ['powershell.exe', '-Command', 'Start-Process', youtube_search_url],\n"
                "                check=True\n"
                "            )\n\n"
                "            self.logger.info(\"YouTube search page opened successfully.\")\n"
                "            return {\n"
                "                \"status\": True,\n"
                "                \"message\": \"YouTube search page opened successfully.\",\n"
                "                \"result\": youtube_search_url\n"
                "            }\n"
                "        except subprocess.CalledProcessError as e:\n"
                "            error_message = f\"Subprocess error: {str(e)}\"\n"
                "            self.logger.error(error_message, exc_info=True)\n"
                "            return {\n"
                "                \"status\": False,\n"
                "                \"message\": error_message,\n"
                "                \"result\": None\n"
                "            }\n"
                "        except Exception as e:\n"
                "            error_message = f\"Failed to open YouTube search for query: {query}. Error: {str(e)}\"\n"
                "            self.logger.error(error_message, exc_info=True)\n"
                "            return {\n"
                "                \"status\": False,\n"
                "                \"message\": error_message,\n"
                "                \"result\": None\n"
                "            }\n\n\n"
                "    def search_products(self, product_id=None, product_name=None, brand=None, price_range=None, stock=None, rating_range=None, \n"
                "                        warranty_years=None, category=None, release_date=None, customer_reviews=None):\n"
                "        \"\"\"\n"
                "        Searches for products in the products CSV file based on the given criteria.\n\n"
                "        Args:\n"
                "            product_id (int, optional): The ID of the product.\n"
                "            product_name (str, optional): The name of the product.\n"
                "            brand (str or list, optional): The brand of the product or a list of brands.\n"
                "            price_range (tuple, optional): The price range as a tuple (min_price, max_price).\n"
                "            stock (int, optional): The stock quantity.\n"
                "            rating_range (tuple, optional): The rating range as a tuple (min_rating, max_rating).\n"
                "            warranty_years (int, optional): The number of warranty years.\n"
                "            category (str, optional): The category of the product.\n"
                "            release_date (str, optional): The release date of the product.\n"
                "            customer_reviews (str, optional): A substring to search for in customer reviews.\n\n"
                "        Returns:\n"
                "            dict: A dictionary containing the status, message, and result (formatted product list or None).\n"
                "        \"\"\"\n"
                "        try:\n"
                "            # Load the CSV file\n"
                "            df = pd.read_csv('flexiai/user_flexiai_rag/data/products.csv')\n\n"
                "            # Apply filters based on the provided arguments\n"
                "            if product_id is not None:\n"
                "                df = df[df['product_id'] == product_id]\n"
                "            if product_name is not None:\n"
                "                df = df[df['product_name'].str.contains(product_name, case=False, na=False)]\n"
                "            if brand is not None:\n"
                "                if isinstance(brand, list):\n"
                "                    df = df[df['brand'].isin(brand)]\n"
                "                else:\n"
                "                    df = df[df['brand'].str.contains(brand, case=False, na=False)]\n"
                "            if price_range is not None:\n"
                "                if isinstance(price_range, tuple) and len(price_range) == 2:\n"
                "                    df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]\n"
                "                else:\n"
                "                    error_message = \"Invalid price range. Provide a tuple with (min_price, max_price).\"\n"
                "                    self.logger.error(error_message)\n"
                "                    return {\n"
                "                        \"status\": False,\n"
                "                        \"message\": error_message,\n"
                "                        \"result\": None\n"
                "                    }\n"
                "            if stock is not None:\n"
                "                df = df[df['stock'] == stock]\n"
                "            if rating_range is not None:\n"
                "                if isinstance(rating_range, tuple) and len(rating_range) == 2:\n"
                "                    df = df[(df['rating'] >= rating_range[0]) & (df['rating'] <= rating_range[1])]\n"
                "                else:\n"
                "                    error_message = \"Invalid rating range. Provide a tuple with (min_rating, max_rating).\"\n"
                "                    self.logger.error(error_message)\n"
                "                    return {\n"
                "                        \"status\": False,\n"
                "                        \"message\": error_message,\n"
                "                        \"result\": None\n"
                "                    }\n"
                "            if warranty_years is not None:\n"
                "                df = df[df['warranty_years'] == warranty_years]\n"
                "            if category is not None:\n"
                "                df = df[df['category'].str.contains(category, case=False, na=False)]\n"
                "            if release_date is not None:\n"
                "                df = df[df['release_date'] == release_date]\n"
                "            if customer_reviews is not None:\n"
                "                df = df[df['customer_reviews'].str.contains(customer_reviews, case=False, na=False)]\n\n"
                "            # Check if any results are found\n"
                "            if df.empty:\n"
                "                return {\n"
                "                    \"status\": False,\n"
                "                    \"message\": \"No products found matching the criteria.\",\n"
                "                    \"result\": None\n"
                "                }\n\n"
                "            # Convert the filtered DataFrame to a list of dictionaries\n"
                "            results = df.to_dict(orient='records')\n"
                "            # Format each product using the format_product function\n"
                "            formatted_results = [format_product(product) for product in results]\n"
                "            return {\n"
                "                \"status\": True,\n"
                "                \"message\": f\"Found {len(formatted_results)} product(s) matching the criteria.\",\n"
                "                \"result\": formatted_results\n"
                "            }\n"
                "        except FileNotFoundError:\n"
                "            error_message = \"The products.csv file was not found.\"\n"
                "            self.logger.error(error_message, exc_info=True)\n"
                "            return {\n"
                "                \"status\": False,\n"
                "                \"message\": error_message,\n"
                "                \"result\": None\n"
                "            }\n"
                "        except pd.errors.EmptyDataError:\n"
                "            error_message = \"The products.csv file is empty.\"\n"
                "            self.logger.error(error_message, exc_info=True)\n"
                "            return {\n"
                "                \"status\": False,\n"
                "                \"message\": error_message,\n"
                "                \"result\": None\n"
                "            }\n"
                "        except Exception as e:\n"
                "            error_message = f\"An error occurred while searching for products: {str(e)}\"\n"
                "            self.logger.error(error_message, exc_info=True)\n"
                "            return {\n"
                "                \"status\": False,\n"
                "                \"message\": error_message,\n"
                "                \"result\": None\n"
                "            }\n\n"
                "    # User can add more custom tasks (assistant personal functions or functions to call other assistants)\n"
            ),
        }
        
        for filename, content in files_content.items():
            file_path = os.path.join(dst_folder, filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"Created file: {file_path}")
    
    def create_env_file(project_root):
        env_file = os.path.join(project_root, '.env')
        if not os.path.exists(env_file):
            with open(env_file, 'w') as f:
                f.write(
                    "# ========================== #\n"
                    "# Example .env file template #\n"
                    "# ========================== #\n\n"
                    "# Your OpenAI API key\n"
                    "OPENAI_API_KEY='your_openai_api_key_here'\n"
                    "# Your Azure OpenAI API key\n"
                    "AZURE_OPENAI_API_KEY='your_azure_openai_api_key_here'\n"
                    "# Your Azure OpenAI endpoint\n"
                    "AZURE_OPENAI_ENDPOINT='your_azure_openai_endpoint_here'\n"
                    "# Azure OpenAI API version\n"
                    "AZURE_OPENAI_API_VERSION='2024-05-01-preview'\n"
                    "# Credential type (either 'openai' or 'azure')\n"
                    "CREDENTIAL_TYPE='openai'\n"
                )
            print(f"Created file: {env_file}")
    
    def create_requirements_file(project_root):
        requirements_file = os.path.join(project_root, 'requirements.txt')
        if not os.path.exists(requirements_file):
            with open(requirements_file, 'w') as f:
                f.write(
                    "annotated-types==0.7.0\n"
                    "anyio==4.4.0\n"
                    "asttokens==2.1.0\n"
                    "azure-common==1.1.28\n"
                    "azure-core==1.30.2\n"
                    "azure-identity==1.17.1\n"
                    "azure-mgmt-core==1.4.0\n"
                    "azure-mgmt-resource==23.1.1\n"
                    "backports.tarfile==1.2.0\n"
                    "blinker==1.8.2\n"
                    "certifi==2024.6.2\n"
                    "cffi==1.16.0\n"
                    "charset-normalizer==3.3.2\n"
                    "click==8.1.7\n"
                    "comm==0.1.3\n"
                    "cryptography==42.0.8\n"
                    "debugpy==1.6.5\n"
                    "decorator==5.1.1\n"
                    "distro==1.9.0\n"
                    "docutils==0.21.2\n"
                    "exceptiongroup==1.1.0\n"
                    "executing==1.2.0\n"
                    "Flask==3.0.3\n"
                    "h11==0.14.0\n"
                    "httpcore==1.0.5\n"
                    "httpx==0.27.0\n"
                    "idna==3.7\n"
                    "importlib_metadata==6.8.0\n"
                    "iniconfig==2.0.0\n"
                    "ipykernel==6.24.0\n"
                    "ipython==8.14.0\n"
                    "ipywidgets==8.1.3\n"
                    "isodate==0.6.1\n"
                    "itsdangerous==2.2.0\n"
                    "jaraco.classes==3.4.0\n"
                    "jaraco.context==5.3.0\n"
                    "jaraco.functools==4.0.1\n"
                    "jedi==0.19.0\n"
                    "jeepney==0.8.0\n"
                    "jupyter_client==8.3.0\n"
                    "jupyter_core==5.2.0\n"
                    "jupyterlab_widgets==3.0.11\n"
                    "keyring==25.2.1\n"
                    "markdown-it-py==3.0.0\n"
                    "MarkupSafe==2.1.5\n"
                    "matplotlib-inline==0.1.6\n"
                    "mdurl==0.1.2\n"
                    "more-itertools==10.3.0\n"
                    "msal==1.29.0\n"
                    "msal-extensions==1.2.0\n"
                    "nest_asyncio==1.5.7\n"
                    "nh3==0.2.17\n"
                    "numpy==2.0.0\n"
                    "openai==1.35.0\n"
                    "packaging==23.1\n"
                    "pandas==2.2.2\n"
                    "parso==0.8.3\n"
                    "pexpect==4.8.0\n"
                    "pickleshare==0.7.5\n"
                    "pkginfo==1.10.0\n"
                    "platformdirs==3.7.0\n"
                    "pluggy==1.5.0\n"
                    "portalocker==2.10.0\n"
                    "prompt_toolkit==3.0.39\n"
                    "psutil==5.9.5\n"
                    "ptyprocess==0.7.0\n"
                    "pure-eval==0.2.2\n"
                    "pycparser==2.22\n"
                    "pydantic==2.7.4\n"
                    "pydantic-settings==2.3.3\n"
                    "pydantic_core==2.18.4\n"
                    "Pygments==2.15.1\n"
                    "PyJWT==2.8.0\n"
                    "pytest==8.2.2\n"
                    "pytest-mock==3.14.0\n"
                    "python-dateutil==2.8.2\n"
                    "python-dotenv==1.0.1\n"
                    "pytz==2024.1\n"
                    "pyzmq==25.1.0\n"
                    "readme_renderer==43.0\n"
                    "requests==2.32.3\n"
                    "requests-toolbelt==1.0.0\n"
                    "rfc3986==2.0.0\n"
                    "rich==13.7.1\n"
                    "SecretStorage==3.3.3\n"
                    "six==1.16.0\n"
                    "sniffio==1.3.1\n"
                    "stack-data==0.6.3\n"
                    "tomli==2.0.1\n"
                    "tornado==6.3.2\n"
                    "tqdm==4.66.4\n"
                    "traitlets==5.10.1\n"
                    "twine==5.1.1\n"
                    "typing_extensions==4.7.1\n"
                    "tzdata==2024.1\n"
                    "urllib3==2.2.2\n"
                    "wcwidth==0.2.6\n"
                    "Werkzeug==3.0.3\n"
                    "widgetsnbextension==4.0.11\n"
                    "zipp==3.17.0\n"
                    "setuptools==70.2.0\n"
                    "pip-audit==2.7.3\n"
                )
            print(f"Created file: {requirements_file}")
    
    if __name__ == '__main__':
        project_root = os.getcwd()
    
        try:
            create_logs_folder(project_root)
            create_user_flexiai_rag_folder(project_root)
            create_env_file(project_root)
            create_requirements_file(project_root)
        except Exception as e:
            print(f"Post-installation step failed: {e}")

</details>

---


### Enable Retrieval-Augmented Generation (RAG)

Running the `post_install.py` script will automatically create the necessary structure and files to enable the Retrieval-Augmented Generation (RAG) module in your project.

Here's an overview of the created structure:

```bash
📦your_project
 ┃
 ┣ 📂user_flexiai_rag
 ┃ ┣ 📂data
 ┃ ┃ ┗ 📜your data files
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜user_function_mapping.py
 ┃ ┣ 📜user_helpers.py             
 ┃ ┗ 📜user_task_manager.py
 ┣ 📂logs
 ┣ 📜requirements.txt
 ┗ 📜.env
 ┣ 
 ...
 ┣ 📂 other folders ...
 ┣ 📜 other files ...
 ┣  ...
```

#### Run the `post_install.py` file to create your starter folders and files.

```bash
python post_install.py
```

### Install Requirements

Install the required dependencies using `pip`.

```bash
pip install -r requirements.txt
```

## Setup

Before using FlexiAI, set up your environment variables. The `post_install.py` script will create a `.env` file in your project root directory with the following template:

```bash
# ========================== #
# Example .env file template #
# ========================== #

# Your OpenAI API key
OPENAI_API_KEY='your_openai_api_key_here'
# Your Azure OpenAI API key
AZURE_OPENAI_API_KEY='your_azure_openai_api_key_here'
# Your Azure OpenAI endpoint
AZURE_OPENAI_ENDPOINT='your_azure_openai_endpoint_here'
# Azure OpenAI API version
AZURE_OPENAI_API_VERSION='2024-05-01-preview'
# Credential type (either 'openai' or 'azure')
CREDENTIAL_TYPE='openai'
```

For more detailed setup instructions, including using virtual environments and troubleshooting, refer to the [Setup Guide](docs/setup.md).

## Usage

### Basic Usage

Here’s a quick example of how to use FlexiAI to interact with OpenAI:

```python
import logging
import os
import platform
from flexiai.core.flexiai_client import FlexiAI
from flexiai.config.logging_config import setup_logging

def clear_console():
    """Clears the console depending on the operating system."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def main():
    # Set up logging using your custom configuration
    # Adjust the logging levels as per your requirements
    setup_logging(root_level=logging.DEBUG, file_level=logging.DEBUG, console_level=logging.ERROR)

    # Initialize FlexiAI
    flexiai = FlexiAI()

    # Use the given assistant ID
    assistant_id = 'asst_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Replace with the actual assistant ID
    
    # Create a new thread
    try:
        thread = flexiai.create_thread()
        thread_id = thread.id
        logging.info(f"Created thread with ID: {thread_id}")
    except Exception as e:
        logging.error(f"Error creating thread: {e}")
        return

    # Variable to store all messages
    all_messages = []
    seen_message_ids = set()

    # Loop to continuously get user input and interact with the assistant
    while True:
        # Get user input
        user_message = input("You: ")

        # Exit the loop if the user types 'exit'
        if user_message.lower() == 'exit':
            print("Exiting...")
            break

        # Run the thread and handle required actions
        try:
            flexiai.create_advanced_run(assistant_id, thread_id, user_message)
            messages = flexiai.retrieve_messages(thread_id, limit=2)  
            
            # Store the extracted messages
            for msg in messages:
                if msg['message_id'] not in seen_message_ids:
                    all_messages.append(msg)
                    seen_message_ids.add(msg['message_id'])

            # Clear console and print the stored messages in the desired format
            clear_console()
            for msg in all_messages:
                role = "🤖 Assistant" if msg['role'] == "assistant" else "🧑 You"
                print(f"{role}: {msg['content']}")
        except Exception as e:
            logging.error(f"Error running thread: {e}")

if __name__ == "__main__":
    main()
```


For detailed usage examples and advanced functionalities, refer to the [Usage Guide](flexiai/docs/usage.md).

## Documentation

The FlexiAI framework comes with comprehensive documentation to help you get started and make the most out of its capabilities:

- [API Reference](flexiai/docs/api_reference.md)
- [Setup Guide](flexiai/docs/setup.md)
- [Usage Guide](flexiai/docs/usage.md)
- [Contributing Guide](flexiai/docs/contributing.md)

## Contributing

We welcome contributions from the community. If you want to contribute to FlexiAI, please read our [Contributing Guide](flexiai/docs/contributing.md) to get started.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.

## Contact

For any inquiries or support, please contact Savin Ionut Razvan at razvan.i.savin@gmail.com.
