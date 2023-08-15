#!/usr/bin/env python3
"""
Created by Jenaide Sibolie
"""


def schools_by_topic(mongo_collection, topic):
    """
    a function that returns the list of schools having a specific topic.
    """
    filtered = {
        "topics": {
            "$elemMatch": {
                "$eq": topic,
            },
        },
    }
    return [document for document in mongo_collection.find(filtered)]
