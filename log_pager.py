import requests
from logger import Logger
from config import ADMIN_API_BASE_URL

"""
log_pager.py

This module contains the LogPager class, which is responsible for fetching logs
from a MongoDB Atlas App Services application using pagination.

Classes:
    LogPager: A class to handle pagination and fetching logs from MongoDB Atlas.
"""


class LogPager:
    """
    A class to handle pagination and fetching logs from MongoDB Atlas.

    Attributes:
        logs_endpoint (str): The endpoint URL for fetching logs.
        query_params (dict): The query parameters for the log request.
        auth_headers (dict): The authorization headers for the log request.
        logger (Logger): The logger instance for logging operations.
    """

    def __init__(self, project_id, app_id, access_token, query_params={}, logger=None):
        """
        Initialize the LogPager with project ID, app ID, access token, query parameters, and logger.

        Args:
            project_id (str): The Atlas Project ID.
            app_id (str): The App ID.
            access_token (str): The access token obtained from MongoDB Atlas.
            query_params (dict, optional): The query parameters for the log request. Defaults to {}.
            logger (Logger, optional): The logger instance for logging operations. Defaults to None.
        """
        self.logs_endpoint = (
            f"{ADMIN_API_BASE_URL}/groups/{project_id}/apps/{app_id}/logs"
        )
        self.query_params = query_params
        self.auth_headers = {"Authorization": f"Bearer {access_token}"}
        self.logger = logger or Logger()

    def get_next_page(self, prev_page=None):
        """
        Fetch the next page of logs.

        Args:
            prev_page (dict, optional): The previous page of logs. Defaults to None.

        Returns:
            dict: The next page of logs.

        Raises:
            Exception: If there are no more pages to fetch.
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        next_end_date = prev_page.get("nextEndDate") if prev_page else None
        self.logger.debug(f"Fetching logs with end date: {next_end_date}")
        next_skip = prev_page.get("nextSkip") if prev_page else None
        self.logger.debug(f"Fetching logs with skip: {next_skip}")
        if prev_page and not next_end_date:
            self.logger.error("Paginated API does not have any more pages.")
            raise Exception("Paginated API does not have any more pages.")

        params = {**self.query_params, "end_date": next_end_date, "skip": next_skip}
        self.logger.debug(f"Fetching logs with params: {params}")
        response = requests.get(
            self.logs_endpoint, headers=self.auth_headers, params=params
        )
        response.raise_for_status()
        return response.json()

    def get_all_logs(self):
        """
        Fetch all logs using pagination.

        Returns:
            list: A list of all logs.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        logs = []
        has_next = True
        prev_page = None
        page_number = 1  # Initialize page counter
        while has_next:
            self.logger.info(
                f"Fetching page {page_number}..."
            )  # Log current page number
            page = self.get_next_page(prev_page)
            logs.extend(page["logs"])
            has_next = "nextEndDate" in page
            prev_page = page
            page_number += 1  # Increment page counter
        return logs
