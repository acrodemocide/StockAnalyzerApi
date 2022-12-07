# StockAnalyzerApi
This API is used for gathering stock data and returning analyses on different asset types and how they can be compared.

# Virtual Environments
This API is written in Python, and so a virtual environment has been set up to isolate the packges installed for this project
from the base Python system.

To activate the virtual environment: venv\Scripts\activate
  You should then see the prompt preceeded by the virtual environment name ((venv) $)
To deactivate the virtual environment: deactivate

To learn more about virtual environments, see https://realpython.com/python-virtual-environments-a-primer/

# Dependencies Installations

We'll use pip freeze to put all of our dependencies in a requirements.txt and install from that file when setting up the dependencies for the project.
This requirements.txt will be tracked in git for the dependencies required for the environment. Whenever dependencies are updated, make sure to update
the requirements.txt file so that it is always up to date.

See https://pip.pypa.io/en/stable/cli/pip_freeze/ for the documentation