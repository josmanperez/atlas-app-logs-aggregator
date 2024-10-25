# MongoDB Atlas Logs Fetcher

This tool is a Python script (`logs.py`) designed to fetch logs from a MongoDB Atlas App Services application using pagination. It supports optional date range filtering and provides a way to authenticate using MongoDB Atlas API keys.

## Features

- Fetch logs from MongoDB Atlas App Services application.
- Supports pagination to handle large sets of logs.
- Optional date range filtering using `start_date` and `end_date` parameters.
- Validates date inputs to ensure they follow the ISO 8601 format.
- Authenticates using MongoDB Atlas public and private API keys.

## Requirements

- Python 3.6 or higher.
- `requirements.txt` library dependencies.

## Installation 

### Create a virtual environment:

```basg
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command-Line Arguments

* `project_id` (required): The Atlas Project ID (hexadecimal string).
app_id (required): The App ID (string).
* `public_api_key` (required): The Atlas Public API Key (string).
* `private_api_key` (required): The Atlas Private API Key (string with hyphens).
* `--start_date` (optional): Start Date in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.MMMZ).
* `--end_date` (optional): End Date in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.MMMZ).
* `--type` (optional): Comma-separated list of supported log types. 

### Example

```bash
python  <project_id> <app_id> <public_api_key> <private_api_key> --start_date 2024-10-05T14:30:00.000Z --end_date 2024-10-06T14:30:00.000Z
```

If `start_date` and `end_date` are not provided, the script will default `start_date` to the last 24 hours from the current time.

### Benefits

* **Automated Log Retrieval**: Easily fetch logs from MongoDB Atlas App Services without manual intervention.
* **Date Range Filtering**: Filter logs by date range to focus on specific periods.
* **Pagination Support**: Handle large sets of logs efficiently using pagination.
* **Validation**: Ensure date inputs are in the correct format to avoid errors.
