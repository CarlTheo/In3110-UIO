.. strompris documentation master file, created by
   sphinx-quickstart on Fri Dec  1 13:10:03 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
=====================================
Welcome to strompris's documentation!
=====================================

Overview
---------

Welcome to the documentation for the Strompris FastAPI project. 
This documentation provides information about the project structure,
functionalities, and instructions for running the application.

Project Contents
-----------------

The project is organized into several components:

1. **`app.py`**: The FastAPI application that serves as the entry point for the Strompris project.
2. **`strompris.py`**: The module containing functions for fetching and plotting electricity prices.
3. **`templates`**: Directory containing HTML templates used by FastAPI.

How to run
-----------

To run the Strompris FastAPI application locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>

2. Install dependencies:
   pip install -r requirements.txt

3. Run the FastAPI application:
   uvicorn app:app --reload
   This will start the FastAPI server, and you can access the application at http://localhost:8000.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   strompris

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
