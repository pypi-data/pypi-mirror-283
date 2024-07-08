# post_install.py
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
            "        tuple: A tuple containing the personal function mappings and assistant function mappings.\n"
            "    \"\"\"\n"
            "    task_manager = UserTaskManager()\n\n"
            "    personal_function_mapping = {\n"
            "        'search_youtube': task_manager.search_youtube,\n"
            "        # Add other functions that call assistant personal functions\n"
            "    }\n\n"
            "    assistant_function_mapping = {\n"
            "        # Add other functions that call assistants here -> the functions must end with \"_assistant\"\n"
            "    }\n\n"
            "    return personal_function_mapping, assistant_function_mapping\n"
        ),
        'user_helpers.py': (
            "# user_flexiai_rag/user_helpers.py\n"
        ),
        'user_task_manager.py': (
            "# user_flexiai_rag/user_task_manager.py\n"
            "import logging\n"
            "from flexiai.config.logging_config import setup_logging\n"
            "import subprocess\n"
            "import urllib.parse\n\n"
            "# Set up logging using your custom configuration\n"
            "setup_logging(root_level=logging.INFO, file_level=logging.DEBUG, console_level=logging.ERROR)\n\n"
            "class UserTaskManager:\n"
            "    \"\"\"\n"
            "    UserTaskManager class handles user-defined tasks.\n"
            "    \"\"\"\n\n"
            "    def __init__(self):\n"
            "        \"\"\"\n"
            "        Initializes the UserTaskManager instance, setting up the logger.\n"
            "        \"\"\"\n"
            "        self.logger = logging.getLogger(__name__)\n\n"
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
            "            subprocess.run(['cmd.exe', '/c', 'start', '', youtube_search_url], check=True)\n\n"
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
            "            }\n"
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
                "OPENAI_API_KEY=your_openai_api_key_here\n"
                "# Your Azure OpenAI API key\n"
                "AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here\n"
                "# Your Azure OpenAI endpoint\n"
                "AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here\n"
                "# Azure OpenAI API version\n"
                "AZURE_OPENAI_API_VERSION=2024-05-01-preview\n"
                "# Credential type (either 'openai' or 'azure')\n"
                "CREDENTIAL_TYPE=openai\n"
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
        