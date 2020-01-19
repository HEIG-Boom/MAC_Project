#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Graph definition
"""
from pyArango.graph import Graph, EdgeDefinition
from pyArango.collection import Collection, Field, Edges


class Users(Collection):
    _fields = {
        "username": Field()
    }


class Series(Collection):
    _fields = {
        "title": Field(),
        "genre": Field()
    }


class Seasons(Collection):
    _fields = {
        "number": Field(),
        "description": Field(),
    }


class Episodes(Collection):
    _fields = {
        "number": Field(),
        "description": Field(),
    }


class Follows(Edges):
    _fields = {
        "start_date": Field()
    }


class Has_seen(Edges):
    _fields = {
        "date": Field()
    }


class Includes(Edges):
    _fields = {}


class Contains(Edges):
    _fields = {}


class SeriesGraph(Graph):
    _edgeDefinitions = [EdgeDefinition("Follows", fromCollections=["Users"], toCollections=["Series"]),
                        EdgeDefinition("Includes", fromCollections=["Series"], toCollections=["Seasons"]),
                        EdgeDefinition("Contains", fromCollections=["Seasons"], toCollections=["Episodes"]),
                        EdgeDefinition("Has_seen", fromCollections=["Users"], toCollections=["Episodes"])]
    _orphanedCollections = []