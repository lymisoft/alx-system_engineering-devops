#!/usr/bin/python3
"""
Module to recursively query the Reddit API and count keyword occurrences in
hot articles for a given subreddit.
"""

import requests
import re
from collections import Counter


def count_words(subreddit, word_list, hot_list=None, after=None):
    """
    Recursively queries the Reddit API and counts occurrences of keywords in
    hot article titles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit to query.
        word_list (list): A list of keywords to count.
        hot_list (list): A list to accumulate the titles of hot articles.
        after (str): The after parameter for pagination.

    Returns:
        None: Prints the counts of keywords.
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
            return

        data = response.json().get("data", {})
        children = data.get("children", [])
        after = data.get("after", None)

        if not children:
            count_and_print(word_list, hot_list)
            return

        hot_list.extend(
            child.get("data", {}).get("title", "").lower()
            for child in children
        )

        # Recursively call the function to get the next page
        count_words(subreddit, word_list, hot_list, after)

    except requests.exceptions.RequestException:
        return


def count_and_print(word_list, hot_list):
    """
    Counts occurrences of keywords in titles and prints the results.

    Args:
        word_list (list): A list of keywords to count.
        hot_list (list): A list of titles to count keywords in.

    Returns:
        None: Prints the counts of keywords.
    """
    # Create a Counter for the keywords
    word_count = Counter()

    # Regex patterns to match keywords exactly
    word_patterns = {
        word: re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        for word in word_list
    }

    for title in hot_list:
        for word, pattern in word_patterns.items():
            word_count[word] += len(pattern.findall(title))

    # Sort by count (desc), then alphabetically (asc)
    sorted_counts = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))

    for word, count in sorted_counts:
        print(f"{word}: {count}")
