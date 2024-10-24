import requests
import argparse
import re
import json

ADMIN_API_BASE_URL = "https://services.cloud.mongodb.com/api/admin/v3.0"


def validate_hex(value):
    """
    validate_hex function checks if the input is a valid hexadecimal string.
    """
    if not re.fullmatch(r"[0-9a-fA-F]+", value):
        raise argparse.ArgumentTypeError(f"{value} is not a valid hexadecimal string")
    return value


def validate_string(value):
    """
    validate_string function checks if the input is a valid string.
    """
    if not isinstance(value, str) or not value.strip():
        raise argparse.ArgumentTypeError(f"{value} is not a valid string")
    return value


def validate_private_key(value):
    """
    validate_private_key function checks if the input is a valid private key format.
    """
    if not re.fullmatch(r"[0-9a-fA-F-]+", value):
        raise argparse.ArgumentTypeError(f"{value} is not a valid private key format")
    return value


def validate_date(value):
    """
    Validate that the given date string follows the ISO 8601 format: YYYY-MM-DDTHH:MM:SS.MMM.

    Args:
        value (str): The date string to validate.

    Returns:
        str: The validated date string.

    Raises:
        argparse.ArgumentTypeError: If the date string does not follow the ISO 8601 format.
    """
    iso_8601_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z"
    if not re.fullmatch(iso_8601_pattern, value):
        raise argparse.ArgumentTypeError(
            f"{value} is not a valid date format. Use 'YYYY-MM-DDTHH:MM:SS.MMMZ'"
        )
    return value


def authenticate(public_api_key, private_api_key):
    """
    Authenticate with MongoDB Atlas using the provided public and private API keys.

    This function sends a POST request to the MongoDB Atlas authentication endpoint
    with the provided public and private API keys. If the authentication is successful,
    it returns the access token.

    Args:
        public_api_key (str): The public API key for MongoDB Atlas.
        private_api_key (str): The private API key for MongoDB Atlas.

    Returns:
        str: The access token obtained from MongoDB Atlas.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.exceptions.RequestException: For other types of request-related errors.
    """
    url = f"{ADMIN_API_BASE_URL}/auth/providers/mongodb-cloud/login"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"username": public_api_key, "apiKey": private_api_key}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["access_token"]


class LogPager:
    def __init__(self, project_id, app_id, access_token, query_params={}):
        self.logs_endpoint = (
            f"{ADMIN_API_BASE_URL}/groups/{project_id}/apps/{app_id}/logs"
        )
        self.query_params = query_params
        self.auth_headers = {"Authorization": f"Bearer {access_token}"}

    def get_next_page(self, prev_page=None):
        next_end_date = prev_page.get("nextEndDate") if prev_page else None
        next_skip = prev_page.get("nextSkip") if prev_page else None
        if prev_page and not next_end_date:
            raise Exception("Paginated API does not have any more pages.")

        params = {**self.query_params, "end_date": next_end_date, "skip": next_skip}
        response = requests.get(
            self.logs_endpoint, headers=self.auth_headers, params=params
        )
        response.raise_for_status()
        return response.json()

    def get_all_logs(self):
        logs = []
        has_next = True
        prev_page = None
        while has_next:
            page = self.get_next_page(prev_page)
            logs.extend(page["logs"])
            has_next = "nextEndDate" in page
            prev_page = page
        return logs


def main():
    parser = argparse.ArgumentParser(
        description="Fetch logs from App Services Application using pagination."
    )
    parser.add_argument(
        "project_id", type=validate_hex, help="Atlas Project ID (hexadecimal string)"
    )
    parser.add_argument("app_id", type=validate_hex, help="App ID (string)")
    parser.add_argument(
        "public_api_key", type=validate_string, help="Atlas Public API Key (string)"
    )
    parser.add_argument(
        "private_api_key",
        type=validate_private_key,
        help="Atlas Private API Key (hexadecimal string)",
    )
    parser.add_argument(
        "--start_date",
        type=validate_date,
        default=None,
        help="Start Date in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.MMM)",
    )
    parser.add_argument(
        "--end_date",
        type=validate_date,
        default=None,
        help="End Date in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.MMM)",
    )

    args = parser.parse_args()
    access_token = authenticate(args.public_api_key, args.private_api_key)
    pager = LogPager(
        args.project_id,
        args.app_id,
        access_token,
        {"start_date": args.start_date, "end_date": args.end_date},
    )
    all_logs = pager.get_all_logs()
    with open("logs.json", "w") as file:
        json.dump(all_logs, file, indent=4)


if __name__ == "__main__":
    main()
