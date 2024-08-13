#!/usr/bin/python3
"""
Module to query the Reddit API and print the titles of the first 10 hot
posts listed for a given subreddit.
"""

import requests


def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10 hot posts
    listed for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit to query.

    Returns:
        None: Prints the titles of the top 10 hot posts.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Reddit API/1.0)"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code != 200:
            print(None)
            return

        data = response.json().get("data", {})
        children = data.get("children", [])

        if not children:
            print(None)
            return

        for child in children[:10]:
            print(child.get("data", {}).get("title", ""))

    except requests.exceptions.RequestException:
        print(None)
