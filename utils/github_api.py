"""GitHub API utility functions for fetching repository information."""

import os
import time
from typing import Dict, Optional, Any
import requests
from requests.exceptions import RequestException

try:
    from loguru import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


def fetch_repository_info(
    owner: str,
    repo: str,
    token: Optional[str] = None,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    """Fetch basic repository information from GitHub API.

    This function retrieves the star count, fork count, and description
    of a GitHub repository using the public GitHub REST API.

    Args:
        owner: Repository owner (username or organization).
        repo: Repository name.
        token: Optional GitHub personal access token for higher rate limits.
        timeout: Request timeout in seconds.

    Returns:
        Dictionary containing repository information with keys:
        - 'stars': Number of stars (int)
        - 'forks': Number of forks (int)
        - 'description': Repository description (str or None)
        - 'full_name': Repository full name (str)
        - 'url': GitHub repository URL (str)
        - 'success': Whether the request succeeded (bool)
        - 'error': Error message if request failed (str or None)

    Raises:
        ValueError: If owner or repo is empty.
        requests.exceptions.RequestException: For network-related errors.
    """
    if not owner or not repo:
        raise ValueError("Owner and repository name must not be empty")

    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    if token:
        headers["Authorization"] = f"token {token}"

    result = {
        "stars": 0,
        "forks": 0,
        "description": None,
        "full_name": f"{owner}/{repo}",
        "url": f"https://github.com/{owner}/{repo}",
        "success": False,
        "error": None,
    }

    try:
        logger.info(f"Fetching repository info for {owner}/{repo}")
        response = requests.get(api_url, headers=headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        result["stars"] = data.get("stargazers_count", 0)
        result["forks"] = data.get("forks_count", 0)
        result["description"] = data.get("description")
        result["success"] = True
        logger.info(f"Successfully fetched info for {owner}/{repo}: "
                    f"{result['stars']} stars, {result['forks']} forks")

    except RequestException as e:
        error_msg = f"Network/HTTP error fetching {owner}/{repo}: {e}"
        logger.error(error_msg)
        result["error"] = str(e)
    except (ValueError, KeyError) as e:
        error_msg = f"Data parsing error for {owner}/{repo}: {e}"
        logger.error(error_msg)
        result["error"] = str(e)
    except Exception as e:
        error_msg = f"Unexpected error fetching {owner}/{repo}: {e}"
        logger.error(error_msg)
        result["error"] = str(e)

    return result


def fetch_repository_info_safe(
    owner: str,
    repo: str,
    token: Optional[str] = None,
    timeout: float = 30.0,
) -> Optional[Dict[str, Any]]:
    """Safely fetch repository info without raising exceptions.

    This is a wrapper around fetch_repository_info that catches all exceptions
    and returns None on failure.

    Args:
        owner: Repository owner (username or organization).
        repo: Repository name.
        token: Optional GitHub personal access token for higher rate limits.
        timeout: Request timeout in seconds.

    Returns:
        Dictionary with repository info on success, None on failure.
    """
    try:
        return fetch_repository_info(owner, repo, token, timeout)
    except Exception as e:
        logger.error(f"Failed to fetch repository info for {owner}/{repo}: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    info = fetch_repository_info("octocat", "Hello-World")
    print(info)
    if info["success"]:
        print(f"Stars: {info['stars']}")
        print(f"Forks: {info['forks']}")
        print(f"Description: {info['description']}")
    else:
        print(f"Error: {info['error']}")