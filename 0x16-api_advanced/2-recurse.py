#!/usr/bin/python3
"""
Module to recursively query the Reddit API and return a list of titles of all
hot articles for a given subreddit.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API and returns a list of all hot articles
    titles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit to query.
        hot_list (list): A list to accumulate the titles of hot articles.
        after (str): The after parameter for pagination.

    Returns:
        list or None: A list of titles if successful, None
        if the subreddit is invalid.
    """
    if hot_list is None:
        hot_list = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Reddit API/1.0)"}
    params = {"after": after} if after else {}

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False
        )

        if response.status_code != 200:
            return None

        data = response.json().get("data", {})
        children = data.get("children", [])
        after = data.get("after", None)

        if not children:
            return hot_list or None

        hot_list.extend(
            child.get("data", {}).get("title", "") for child in children
        )

        return recurse(subreddit, hot_list, after)

    except requests.exceptions.RequestException:
        return None
