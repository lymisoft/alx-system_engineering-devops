#!/usr/bin/python3
"""
Module to query the Reddit API and print the titles of the first 10 hot posts
from a given subreddit.
"""

import requests

def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10 hot posts
    for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit to query.

    Returns:
        None: If the subreddit is invalid or there are issues with the API call.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Reddit API/1.0)"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code != 200:
            print(None)
            return

        results = response.json().get("data", {})
        children = results.get("children", [])

        for i in range(min(10, len(children))):
            title = children[i].get("data", {}).get("title", "")
            print(title)

    except requests.exceptions.RequestException:
        print(None)

