# Power BI XMLA Endpoint Download to Parquet

This package allows you to fetch and save Power BI tables in Parquet format via the XMLA endpoint.

## System Requirements

This package requires a Windows environment with .NET assemblies, as it relies on `pythonnet` to interact with .NET libraries.

## Authentication

The package currently only supports authentication using the Microsoft Authentication Library (MSAL) to obtain an access token, supporting Multi-Factor Authentication (MFA).


## Python Version Requirement

This package requires Python version >=3.9,<3.13.

## Installation

### Using Poetry

To install the package using Poetry, run:

poetry add download_pbi_xmla

### Using pip

To install the package using pip, run:

pip install download_pbi_xmla

## Setup

1. Copy the example environment and config files:
cp .env.example .env
cp config.example.json config.json

2. Edit the .env and config.json files with your credentials and configuration.

### .env File Example

CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
TENANT_ID=your-tenant-id
CONFIG_FILE=config.json
SAVE_PATH=./data

### config.json File Example

{
  "server": "your-server-url",
  "database": "your-database-name",
  "tables": [
    {
      "name": "your-table-name",
      "refresh_type": "full",
      "date_column": "your-date-column",
      "last_date": "YYYY-MM-DD"
    }
  ]
}

## Usage

After setting up the environment and configuration files, you can use the download.py script to fetch and save Power BI tables in Parquet format.

### Running the Script

You can run the script directly:

python download.py

### Logging

Logs are saved in the logs directory with a timestamp. Both file and console logging are set up to capture the script's execution details.


## Example Workflow

Here’s an example workflow of how to use the package:

1. Install the package using Poetry or pip.
2. Copy and configure the .env and config.json files.
3. Run the download.py script to fetch and save Power BI tables.

## Script Overview

- download_pbi_xmla/main.py: Contains the main functionality to fetch and save tables.
- download.py: Script to execute the main functionality defined in main.py.

## Command Syntax

The script fetches configuration from environment variables and the config file. 
There is no need to provide command-line arguments, making the usage straightforward.

### Example Command

Simply run:
python download.py

## Contribution

Feel free to fork the repository and create pull requests. Contributions are welcome!

For any issues or feature requests, please open an issue on the repository.