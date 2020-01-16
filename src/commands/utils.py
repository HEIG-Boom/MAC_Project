#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contains a few helper functions for the main bot commands
"""


def build_menu(buttons, number_columns):
    menu = [buttons[i:i + number_columns] for i in range(0, len(buttons), number_columns)]

    return menu
