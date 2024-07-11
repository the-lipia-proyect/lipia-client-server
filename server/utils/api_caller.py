import requests
from typing import Any, Dict, Optional

from utils.logger import get_logger

logger = get_logger("APILogger")


def api_caller(
    method: str, headers: Dict[str, Any], url: str, body: Optional[Any] = None
):
    """
    Make an API call using the specified HTTP method, headers, URL, and payload.

    Args:
        method (str): The HTTP method to use (e.g., "GET", "POST", "PUT", "DELETE").
        headers (dict): A dictionary of HTTP headers.
        url (str): The URL of the API endpoint.
        body (dict or bytes, optional): The payload data to send (for POST, PUT, etc.).

    Returns:
        requests.Response: The response object from the API call.
    """
    logger.info(f"Calling api to:{url}, with headers : {headers} and payload: {body}")
    response = requests.request(method=method, url=url, headers=headers, data=body)
    response.raise_for_status()
    return response.json()
