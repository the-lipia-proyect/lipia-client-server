import http
from typing import Dict, Any

from flask import jsonify


def base_response(body: Dict[str, Any], status_code: http.HTTPStatus) -> jsonify:
    """
    Creates a standardized response for Flask applications.

    This function serves as the foundation for building various response functions
    like `ok`, `bad_request`, etc. It takes a dictionary containing the response
    body and an HTTP status code and returns a Flask response object.

    Args:
        body (Dict[str, Any]): The dictionary containing the response data.
        status_code (http.HTTPStatus): The HTTP status code for the response.

    Returns:
        jsonify: A Flask response object with the specified body and status code.
    """

    return jsonify(body), status_code


def ok(body: Dict[str, Any]) -> jsonify:
    """
    Returns a successful response (HTTP status code 200) with the provided body.

    This function is a convenient shortcut for creating successful responses from
    your Flask routes.

    Args:
        body (Dict[str, Any]): The dictionary containing the response data.

    Returns:
        jsonify: A Flask response object with the provided body and a 200 status code.
    """

    return base_response(body, http.HTTPStatus.OK)


def bad_request(body: Dict[str, Any]) -> jsonify:
    """
    Returns a bad request response (HTTP status code 400) with the provided body.

    This function is typically used when the request from the client is invalid,
    e.g., missing required parameters or containing malformed data.

    Args:
        body (Dict[str, Any]): The dictionary containing the response data.

    Returns:
        jsonify: A Flask response object with the provided body and a 400 status code.
    """

    return base_response(body, http.HTTPStatus.BAD_REQUEST)


def unauthorized(body: Dict[str, Any]) -> jsonify:
    """
    Returns an unauthorized response (HTTP status code 401) with the provided body.

    This function is used when a client attempts to access a resource without
    proper authentication credentials.

    Args:
        body (Dict[str, Any]): The dictionary containing the response data.

    Returns:
        jsonify: A Flask response object with the provided body and a 401 status code.
    """

    return base_response(body, http.HTTPStatus.UNAUTHORIZED)


def not_found(body: Dict[str, Any]) -> jsonify:
    """
    Returns a not found response (HTTP status code 404) with the provided body.

    This function is used when a client requests a resource that does not exist
    on the server.

    Args:
        body (Dict[str, Any]): The dictionary containing the response data.

    Returns:
        jsonify: A Flask response object with the provided body and a 404 status code.
    """

    return base_response(body, http.HTTPStatus.NOT_FOUND)


def internal_server_error(body: Dict[str, Any]) -> jsonify:
    """
    Returns an internal server error response (HTTP status code 500) with the provided body.

    This function is used when an unexpected error occurs on the server side
    during request processing. It's generally recommended to keep the response body
    minimal for security reasons.

    Args:
        body (Dict[str, Any]): The dictionary containing the response data.
        Consider providing minimal information or a generic message for security reasons.

    Returns:
        jsonify: A Flask response object with the provided body and a 500 status code.
    """

    return base_response(body, http.HTTPStatus.INTERNAL_SERVER_ERROR)
