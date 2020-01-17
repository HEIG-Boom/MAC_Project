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


class Follows(Edges):
    _fields = {
        "start_date": Field()
    }


class SeriesGraph(Graph):
    _edgeDefinitions = [EdgeDefinition("Follows", fromCollections=["Users"], toCollections=["Series"])]
    _orphanedCollections = []