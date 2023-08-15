#!/usr/bin/env python3
"""
Created by Jenaide Sibolie
"""


def insert_school(mongo_collection, **kwargs):
    """
    a function that inserts a new document in a collection
    based on kwargs.
    """
    school = mongo_collection.insert_one(kwargs)
    return school.inserted_id
