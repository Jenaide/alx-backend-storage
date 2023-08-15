#!/usr/bin/env python3
"""
Created by Jenaide Sibolie
"""


def list_all(mongo_collection):
    """
    A function that lists all documents in a collection
    """
    return [document for document in mongo_collection.find()]
