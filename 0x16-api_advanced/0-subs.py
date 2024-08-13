#!/usr/bin/python3
"""
Module to interact with the Reddit API and return the number of subscribers
for a given subreddit.
"""

import requests


def number_of_subscribers(subreddit):
    """
    Queries the Reddit API and returns the number of subscribers for a
    given subreddit.

    Args:
        subreddit (str): The name of the subreddit to query.

    Returns:
        int: The number of subscribers, or 0 if the subreddit is invalid.
    """
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Reddit API/1.0)"
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code != 200:
            return 0

        results = response.json().get("data", {})
        return results.get("subscribers", 0)

    except requests.exceptions.RequestException:
        return 0
    except ValueError:
        return 0
